namespace WebApplication2.Models;

public sealed class ProductCard
{
    public string Slug { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string NameHindi { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string DescriptionHindi { get; set; } = string.Empty;
    public string ImageUrl { get; set; } = string.Empty;
    public string Url { get; set; } = "#";
    public string Price { get; set; } = string.Empty;
    public decimal PriceAmount { get; set; }
    public string? Badge { get; set; }
    public string? BadgeHindi { get; set; }
}
