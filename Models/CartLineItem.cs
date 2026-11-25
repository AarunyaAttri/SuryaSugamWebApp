namespace WebApplication2.Models;

public sealed class CartLineItem
{
    public string Id { get; set; } = string.Empty;
    public string CustomerId { get; set; } = string.Empty;
    public string Slug { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string NameHindi { get; set; } = string.Empty;
    public string ImageUrl { get; set; } = string.Empty;
    public decimal UnitPrice { get; set; }
    public int Quantity { get; set; }
    public string Size { get; set; } = string.Empty;
    public string EggOption { get; set; } = string.Empty;
    public string City { get; set; } = string.Empty;
    public string Area { get; set; } = string.Empty;
    public DateTime DeliveryDate { get; set; }
    public string TimeSlot { get; set; } = string.Empty;
    public string? Message { get; set; }
}
