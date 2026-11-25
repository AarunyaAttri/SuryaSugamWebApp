namespace WebApplication2.Models;

public sealed class StorefrontViewModel
{
    public string Announcement { get; set; } = string.Empty;
    public string HeroEyebrow { get; set; } = string.Empty;
    public string HeroEyebrowHindi { get; set; } = string.Empty;
    public string HeroTitle { get; set; } = string.Empty;
    public string HeroTitleHindi { get; set; } = string.Empty;
    public string HeroDescription { get; set; } = string.Empty;
    public string HeroDescriptionHindi { get; set; } = string.Empty;
    public string HeroImageUrl { get; set; } = string.Empty;
    public List<NavigationLink> Navigation { get; set; } = [];
    public List<CategoryCard> Categories { get; set; } = [];
    public List<ProductCard> Fans { get; set; } = [];
    public List<ProductCard> CreamRolls { get; set; } = [];
    public List<ProductCard> Toasts { get; set; } = [];
    public List<TestimonialCard> Testimonials { get; set; } = [];
    public NewsletterInput Newsletter { get; set; } = new();
    public CustomOrderInput CustomOrder { get; set; } = new();
}
