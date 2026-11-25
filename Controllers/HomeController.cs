using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Diagnostics;
using System.Globalization;
using System.Text.Json;
using WebApplication2.Data;
using WebApplication2.Models;
using WebApplication2.Services;

namespace WebApplication2.Controllers;

public class HomeController : Controller
{
    private readonly AppDbContext _database;

    public HomeController(AppDbContext database)
    {
        _database = database;
    }

    public async Task<IActionResult> Index()
    {
        var model = CreateStorefront();
        await SetLayoutDataAsync();
        return View(model);
    }

    [HttpGet("/products/{slug}", Name = "ProductDetails")]
    public async Task<IActionResult> Product(string slug)
    {
        var (product, category) = FindProduct(slug);
        if (product is null)
        {
            return NotFound();
        }

        var model = CreateProductDetail(product, category);
        await SetProductPageViewDataAsync(product);
        return View(model);
    }

    [HttpPost("/products/{slug}/add")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> AddToCart(string slug, [Bind(Prefix = "Order")] ProductOrderInput order)
    {
        var (product, category) = FindProduct(slug);
        if (product is null)
        {
            return NotFound();
        }

        var model = CreateProductDetail(product, category);
        if (!model.SizeOptions.Contains(order.Size))
        {
            ModelState.AddModelError("Order.Size", "Choose an available size.");
        }

        if (!model.EggOptions.Contains(order.EggOption))
        {
            ModelState.AddModelError("Order.EggOption", "Choose an available option.");
        }

        if (!model.TimeSlots.Contains(order.TimeSlot))
        {
            ModelState.AddModelError("Order.TimeSlot", "Choose an available delivery time.");
        }

        if (order.DeliveryDate.HasValue && order.DeliveryDate.Value.Date < GetBakeryToday())
        {
            ModelState.AddModelError("Order.DeliveryDate", "Choose today or a future date.");
        }

        if (!ModelState.IsValid)
        {
            model.Order = order;
            await SetProductPageViewDataAsync(product);
            return View("Product", model);
        }

        var customerId = CustomerIdentity.GetOrCreate(HttpContext);
        var trimmedArea = order.Area.Trim();
        var trimmedMessage = string.IsNullOrWhiteSpace(order.Message) ? null : order.Message.Trim();
        var cartItem = new CartLineItem
        {
            Id = Guid.NewGuid().ToString("N"),
            CustomerId = customerId,
            Slug = product.Slug,
            Name = product.Name,
            NameHindi = product.NameHindi,
            ImageUrl = product.ImageUrl,
            UnitPrice = product.PriceAmount,
            Quantity = order.Quantity,
            Size = order.Size,
            EggOption = order.EggOption,
            City = order.City,
            Area = trimmedArea,
            DeliveryDate = order.DeliveryDate!.Value,
            TimeSlot = order.TimeSlot,
            Message = trimmedMessage
        };
        _database.CartItems.Add(cartItem);
        _database.CustomerResponseEvents.Add(new CustomerResponseEvent
        {
            CustomerId = customerId,
            EventType = "ProductAddedToCart",
            ProductSlug = product.Slug,
            ResponseJson = JsonSerializer.Serialize(new { product.Name, Order = order })
        });
        await _database.SaveChangesAsync();
        TempData["CartMessage"] = $"{order.Quantity} × {product.Name} added to your cart.";
        return RedirectToRoute("ProductDetails", new { slug = product.Slug });
    }

    [HttpGet("/cart", Name = "ShoppingCart")]
    public async Task<IActionResult> Cart()
    {
        await SetLayoutDataAsync();
        var customerId = CustomerIdentity.GetOrCreate(HttpContext);
        return View(new CartViewModel { Items = await GetCartItemsAsync(customerId) });
    }

    [HttpPost("/cart/update")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> UpdateCart(CartQuantityInput input)
    {
        if (ModelState.IsValid)
        {
            var customerId = CustomerIdentity.GetOrCreate(HttpContext);
            var item = await _database.CartItems.SingleOrDefaultAsync(item => item.Id == input.Id && item.CustomerId == customerId);
            if (item is not null)
            {
                item.Quantity = input.Quantity;
                _database.CustomerResponseEvents.Add(new CustomerResponseEvent
                {
                    CustomerId = customerId,
                    EventType = "CartQuantityUpdated",
                    ProductSlug = item.Slug,
                    ResponseJson = JsonSerializer.Serialize(new { item.Id, item.Quantity })
                });
                await _database.SaveChangesAsync();
                TempData["CartMessage"] = "Cart quantity updated.";
            }
        }

        return RedirectToRoute("ShoppingCart");
    }

    [HttpPost("/cart/remove")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> RemoveFromCart(string id)
    {
        var customerId = CustomerIdentity.GetOrCreate(HttpContext);
        var item = await _database.CartItems.SingleOrDefaultAsync(item => item.Id == id && item.CustomerId == customerId);
        if (item is not null)
        {
            _database.CustomerResponseEvents.Add(new CustomerResponseEvent
            {
                CustomerId = customerId,
                EventType = "CartItemRemoved",
                ProductSlug = item.Slug,
                ResponseJson = JsonSerializer.Serialize(item)
            });
            _database.CartItems.Remove(item);
            await _database.SaveChangesAsync();
            TempData["CartMessage"] = "Item removed from your cart.";
        }

        return RedirectToRoute("ShoppingCart");
    }

    [HttpPost("/cart/checkout")]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Checkout(string? language)
    {
        var customerId = CustomerIdentity.GetOrCreate(HttpContext);
        var cartItems = await GetCartItemsAsync(customerId);
        if (cartItems.Count == 0)
        {
            return RedirectToRoute("ShoppingCart");
        }

        var selectedLanguage = language == "hi" ? "hi" : "en";
        var order = new CustomerOrderRecord
        {
            CustomerId = customerId,
            Language = selectedLanguage,
            Subtotal = cartItems.Sum(item => item.UnitPrice * item.Quantity),
            Items = cartItems.Select(item => new CustomerOrderItemRecord
            {
                ProductSlug = item.Slug,
                ProductName = item.Name,
                ProductNameHindi = item.NameHindi,
                ImageUrl = item.ImageUrl,
                UnitPrice = item.UnitPrice,
                Quantity = item.Quantity,
                Size = item.Size,
                EggOption = item.EggOption,
                City = item.City,
                Area = item.Area,
                DeliveryDate = item.DeliveryDate,
                TimeSlot = item.TimeSlot,
                Message = item.Message
            }).ToList()
        };

        _database.CustomerOrders.Add(order);
        _database.CustomerResponseEvents.Add(new CustomerResponseEvent
        {
            CustomerId = customerId,
            EventType = "OrderSubmitted",
            ResponseJson = JsonSerializer.Serialize(order)
        });
        _database.CartItems.RemoveRange(cartItems);
        await _database.SaveChangesAsync();

        var message = selectedLanguage == "hi"
            ? $"नमस्ते सूर्यसुगम बेकरी, मुझे यह ऑर्डर करना है: {string.Join("; ", cartItems.Select(item => $"{item.Quantity} x {item.NameHindi} ({item.Size}, {item.EggOption}, {item.City}, {item.Area}, {item.DeliveryDate.ToString("dd MMM yyyy", CultureInfo.InvariantCulture)}, {item.TimeSlot}{(string.IsNullOrWhiteSpace(item.Message) ? string.Empty : $", संदेश: {item.Message}")})"))}। अनुमानित कुल: ₹{order.Subtotal:N0}।"
            : $"Hello SuryaSugam Bakery, I would like to order: {string.Join("; ", cartItems.Select(item => $"{item.Quantity} x {item.Name} ({item.Size}, {item.EggOption}, {item.City}, {item.Area}, {item.DeliveryDate.ToString("dd MMM yyyy", CultureInfo.InvariantCulture)}, {item.TimeSlot}{(string.IsNullOrWhiteSpace(item.Message) ? string.Empty : $", Note: {item.Message}")})"))}. Estimated total: ₹{order.Subtotal:N0}.";

        return Redirect($"https://wa.me/918921986080?text={Uri.EscapeDataString(message)}");
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> Subscribe([Bind(Prefix = "Newsletter")] NewsletterInput input)
    {
        if (!ModelState.IsValid)
        {
            var model = CreateStorefront();
            model.Newsletter = input;
            await SetLayoutDataAsync();
            return View("Index", model);
        }

        var customerId = CustomerIdentity.GetOrCreate(HttpContext);
        var subscription = new NewsletterSubscription { CustomerId = customerId, Email = input.Email.Trim() };
        _database.NewsletterSubscriptions.Add(subscription);
        _database.CustomerResponseEvents.Add(new CustomerResponseEvent
        {
            CustomerId = customerId,
            EventType = "NewsletterSubscribed",
            ResponseJson = JsonSerializer.Serialize(new { subscription.Email })
        });
        await _database.SaveChangesAsync();
        TempData["NewsletterMessage"] = "Thanks for subscribing! We’ll share fresh bakery updates with you.";
        return RedirectToAction(nameof(Index));
    }

    [HttpPost]
    [ValidateAntiForgeryToken]
    public async Task<IActionResult> CustomOrder(CustomOrderInput input)
    {
        var supportedProducts = new[] { "Fans", "CreamRoll", "Toast", "Other bakery item" };
        if (!supportedProducts.Contains(input.Product, StringComparer.Ordinal))
        {
            ModelState.AddModelError(nameof(input.Product), "Choose a valid product.");
        }

        if (input.PreferredDate.HasValue && input.PreferredDate.Value.Date < GetBakeryToday())
        {
            ModelState.AddModelError(nameof(input.PreferredDate), "Choose today or a future date.");
        }

        if (input.Language is not ("en" or "hi"))
        {
            input.Language = "en";
        }

        if (!ModelState.IsValid)
        {
            var model = CreateStorefront();
            model.CustomOrder = input;
            await SetLayoutDataAsync();
            return View("Index", model);
        }

        input.CustomerName = input.CustomerName.Trim();
        input.Phone = input.Phone.Trim();
        input.Occasion = input.Occasion?.Trim();
        input.Details = input.Details.Trim();
        var customerId = CustomerIdentity.GetOrCreate(HttpContext);
        var request = new CustomOrderRequestRecord
        {
            CustomerId = customerId,
            CustomerName = input.CustomerName,
            Phone = input.Phone,
            Product = input.Product,
            Quantity = input.Quantity,
            Occasion = input.Occasion,
            PreferredDate = input.PreferredDate,
            Details = input.Details,
            Language = input.Language
        };
        _database.CustomOrderRequests.Add(request);
        _database.CustomerResponseEvents.Add(new CustomerResponseEvent
        {
            CustomerId = customerId,
            EventType = "CustomOrderSubmitted",
            ResponseJson = JsonSerializer.Serialize(input)
        });
        await _database.SaveChangesAsync();

        var message = input.Language == "hi"
            ? $"नमस्ते सूर्यसुगम बेकरी, मैं कस्टम ऑर्डर देना चाहता/चाहती हूँ। नाम: {input.CustomerName}। फ़ोन / व्हाट्सऐप: {input.Phone}। उत्पाद: {input.Product}। मात्रा: {input.Quantity}। {(string.IsNullOrWhiteSpace(input.Occasion) ? string.Empty : $"अवसर: {input.Occasion}। ")}{(input.PreferredDate.HasValue ? $"पसंदीदा तारीख: {input.PreferredDate:dd MMM yyyy}। " : string.Empty)}कस्टम जानकारी: {input.Details}"
            : $"Hello SuryaSugam Bakery, I would like to place a custom order. Name: {input.CustomerName}. Phone / WhatsApp: {input.Phone}. Product: {input.Product}. Quantity: {input.Quantity}. {(string.IsNullOrWhiteSpace(input.Occasion) ? string.Empty : $"Occasion: {input.Occasion}. ")}{(input.PreferredDate.HasValue ? $"Preferred date: {input.PreferredDate:dd MMM yyyy}. " : string.Empty)}Customization details: {input.Details}";

        return Redirect($"https://wa.me/918921986080?text={Uri.EscapeDataString(message)}");
    }

    public async Task<IActionResult> Privacy()
    {
        await SetLayoutDataAsync();
        return View();
    }

    [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
    public async Task<IActionResult> Error()
    {
        try
        {
            await SetLayoutDataAsync();
        }
        catch
        {
            ViewData["CartCount"] = 0;
        }

        return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
    }

    public static bool IsKnownProductSlug(string slug) => FindProduct(slug).Product is not null;

    public static DateTime GetBakeryToday()
    {
        try
        {
            var istZone = TimeZoneInfo.FindSystemTimeZoneById("Asia/Kolkata");
            return TimeZoneInfo.ConvertTimeFromUtc(DateTime.UtcNow, istZone).Date;
        }
        catch (TimeZoneNotFoundException)
        {
            return DateTime.UtcNow.AddMinutes(330).Date;
        }
    }

    private async Task SetLayoutDataAsync()
    {
        ViewData["Navigation"] = CreateStorefront().Navigation;
        var customerId = CustomerIdentity.GetOrCreate(HttpContext);
        ViewData["CartCount"] = await _database.CartItems
            .Where(item => item.CustomerId == customerId)
            .SumAsync(item => (int?)item.Quantity) ?? 0;
    }

    private Task<List<CartLineItem>> GetCartItemsAsync(string customerId) =>
        _database.CartItems.AsNoTracking().Where(item => item.CustomerId == customerId).ToListAsync();

    private async Task SetProductPageViewDataAsync(ProductCard product)
    {
        ViewData["Title"] = product.Name;
        await SetLayoutDataAsync();
    }

    private static (ProductCard? Product, string Category) FindProduct(string slug)
    {
        var store = CreateStorefront();
        var sections = new[]
        {
            (store.Fans, "Fans"),
            (store.CreamRolls, "CreamRoll"),
            (store.Toasts, "Toast")
        };

        foreach (var (products, category) in sections)
        {
            var product = products.FirstOrDefault(item => string.Equals(item.Slug, slug, StringComparison.OrdinalIgnoreCase));
            if (product is not null)
            {
                return (product, category);
            }
        }

        return (null, string.Empty);
    }

    private static ProductDetailViewModel CreateProductDetail(ProductCard product, string category) => new()
    {
        Product = product,
        Category = category,
        CategoryHindi = category switch
        {
            "Fans" => "फैन",
            "CreamRoll" => "क्रीम रोल",
            _ => "टोस्ट"
        },
        Description = $"{product.Description}. Freshly prepared in small batches at SuryaSugam Bakery.",
        DescriptionHindi = $"{product.DescriptionHindi}। सूर्यसुगम बेकरी में छोटी मात्रा में ताज़ा तैयार।",
        CareInstructions = "Enjoy fresh on the day of delivery. Store in an airtight container and keep away from direct sunlight.",
        SizeOptions = category switch
        {
            "Fans" => ["Pack of 2", "Pack of 4", "Pack of 8"],
            "CreamRoll" => ["1 piece", "Box of 4", "Box of 6"],
            _ => ["200 g", "400 g", "800 g"]
        },
        EggOptions = ["Regular", "Eggless"],
        TimeSlots = ["10:00 AM – 12:00 PM", "12:00 PM – 2:00 PM", "2:00 PM – 5:00 PM", "5:00 PM – 8:00 PM"],
        Order = new()
    };

    private static StorefrontViewModel CreateStorefront() => new()
    {
        Announcement = "Freshly baked in Mathura — made for your tea-time",
        HeroEyebrow = "Fresh from the oven · Made in Mathura",
        HeroEyebrowHindi = "मथुरा में ताज़ा बेक किया हुआ",
        HeroTitle = "A little more joy with every bite.",
        HeroTitleHindi = "हर निवाले में थोड़ी और खुशी।",
        HeroDescription = "Flaky Fans, soft CreamRoll, and crisp Toast, made fresh for your everyday tea-time.",
        HeroDescriptionHindi = "कुरकुरे फैन, मुलायम क्रीम रोल और ताज़ा टोस्ट — आपकी रोज़ की चाय के साथ।",
        HeroImageUrl = "/images/home%20page.jpeg",
        Navigation =
        [
            new() { Label = "Fans", Url = "/#fans", Children = [new() { Label = "Mini Fan", Url = "/#fans" }, new() { Label = "Standard Fan", Url = "/#fans" }, new() { Label = "Large Fan", Url = "/#fans" }] },
            new() { Label = "CreamRoll", Url = "/#creamroll" },
            new() { Label = "Toast", Url = "/#toast", Children = [new() { Label = "Mini Toast", Url = "/#toast" }, new() { Label = "Standard Toast", Url = "/#toast" }, new() { Label = "Large Toast", Url = "/#toast" }] },
            new() { Label = "Our story", Url = "/#our-story" }
        ],
        Categories =
        [
            new() { Name = "Fans", NameHindi = "फैन", Description = "Flaky favourites for tea-time", DescriptionHindi = "चाय के साथ कुरकुरे और स्वादिष्ट", ImageUrl = "/images/fans-product.png", Url = "#fans", Badge = "Fresh batch", BadgeHindi = "ताज़ा" },
            new() { Name = "CreamRoll", NameHindi = "क्रीम रोल", Description = "Soft rolls with a creamy centre", DescriptionHindi = "मुलायम रोल, अंदर स्वादिष्ट क्रीम", ImageUrl = "/images/creamroll.jpeg", Url = "#creamroll" },
            new() { Name = "Toast", NameHindi = "टोस्ट", Description = "Crisp, golden, and easy to share", DescriptionHindi = "कुरकुरा, सुनहरा और सबके साथ बाँटने के लिए", ImageUrl = "/images/toast.jpeg", Url = "#toast" },
            new() { Name = "Special Request", NameHindi = "विशेष ऑर्डर", Description = "Create a custom bakery order", DescriptionHindi = "अपनी पसंद का खास बेकरी ऑर्डर दें", ImageUrl = "/images/special-request-illustration.svg", Url = "#custom-order", Badge = "Custom order", BadgeHindi = "कस्टम ऑर्डर" }
        ],
        Fans =
        [
            new() { Slug = "fan-puff", Name = "Mini Fan", NameHindi = "मिनी फैन", Description = "Golden, flaky tea-time pastry", DescriptionHindi = "सुनहरी, कुरकुरी चाय-समय पेस्ट्री", ImageUrl = "/images/fans-product.png", Url = "#fans", Price = "₹145", PriceAmount = 145m, Badge = "Bestseller", BadgeHindi = "सबसे पसंदीदा" },
            new() { Slug = "masala-fan", Name = "Standard Fan", NameHindi = "स्टैंडर्ड फैन", Description = "A crisp, savoury chai companion", DescriptionHindi = "चाय के साथ कुरकुरा, मसालेदार स्वाद", ImageUrl = "/images/fan2.jpeg", Url = "#fans", Price = "₹160", PriceAmount = 160m },
            new() { Slug = "paneer-fan", Name = "Large Fan", NameHindi = "बड़ा फैन", Description = "Flaky pastry with a spiced filling", DescriptionHindi = "मसालेदार पनीर की भरावन वाली कुरकुरी पेस्ट्री", ImageUrl = "/images/fan3.jpeg", Url = "#fans", Price = "₹180", PriceAmount = 180m, Badge = "New", BadgeHindi = "नया" }
        ],
        CreamRolls =
        [
            new() { Slug = "creamroll", Name = "CreamRoll", NameHindi = "क्रीम रोल", Description = "A soft roll with a smooth cream filling", DescriptionHindi = "मुलायम क्रीम से भरा स्वादिष्ट रोल", ImageUrl = "/images/creamroll.jpeg", Url = "#creamroll", Price = "₹60", PriceAmount = 60m, Badge = "Bestseller", BadgeHindi = "सबसे पसंदीदा" }
        ],
        Toasts =
        [
            new() { Slug = "milk-toast", Name = "Mini Toast", NameHindi = "मिनी टोस्ट", Description = "A smaller pack of crisp toast for a quick tea break", DescriptionHindi = "चाय के साथ हल्के नाश्ते के लिए कुरकुरा टोस्ट का छोटा पैक", ImageUrl = "/images/minitoast.jpg", Url = "#toast", Price = "₹100", PriceAmount = 100m, Badge = "Bestseller", BadgeHindi = "सबसे पसंदीदा" },
            new() { Slug = "classic-rusk-toast", Name = "Standard Toast", NameHindi = "स्टैंडर्ड टोस्ट", Description = "Our everyday-sized pack of crisp, golden toast", DescriptionHindi = "रोज़ के लिए कुरकुरे, सुनहरे टोस्ट का पैक", ImageUrl = "/images/toast.jpeg", Url = "#toast", Price = "₹120", PriceAmount = 120m },
            new() { Slug = "fruit-toast", Name = "Large Toast", NameHindi = "बड़ा टोस्ट", Description = "A larger pack of crisp toast, perfect for sharing", DescriptionHindi = "सबके साथ बाँटने के लिए कुरकुरे टोस्ट का बड़ा पैक", ImageUrl = "/images/largetoast.png", Url = "#toast", Price = "₹150", PriceAmount = 150m, Badge = "Fresh batch", BadgeHindi = "ताज़ा" }
        ],
        Testimonials =
        [
            new() { Quote = "The Mini Fan was crisp, fresh, and perfect with evening chai. We ordered another pack the next day.", QuoteHindi = "मिनी फैन कुरकुरा और ताज़ा था, शाम की चाय के साथ बहुत अच्छा लगा। अगले दिन हमने फिर मंगाया।", CustomerName = "Ananya M.", Location = "Mathura", Initials = "AM" },
            new() { Quote = "Soft CreamRoll and delicious Toast arrived fresh. A lovely local bakery for our family.", QuoteHindi = "क्रीम रोल मुलायम और टोस्ट स्वादिष्ट व ताज़ा था। हमारे परिवार के लिए मथुरा की बढ़िया बेकरी।", CustomerName = "Rhea K.", Location = "Ram Nagar", Initials = "RK" },
            new() { Quote = "The flavours are comforting and the snacks are always fresh. SuryaSugam is now our tea-time favourite.", QuoteHindi = "स्वाद बहुत अच्छा है और स्नैक्स हमेशा ताज़ा मिलते हैं। अब सुर्यसुगम हमारी चाय-समय की पसंदीदा जगह है।", CustomerName = "Kabir S.", Location = "Lohaban", Initials = "KS" }
        ]
    };
}
