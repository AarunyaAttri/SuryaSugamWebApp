namespace WebApplication2.Models;

public sealed class ProductDetailViewModel
{
    public ProductCard Product { get; set; } = new();
    public string Category { get; set; } = string.Empty;
    public string CategoryHindi { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string DescriptionHindi { get; set; } = string.Empty;
    public string CareInstructions { get; set; } = string.Empty;
    public List<string> SizeOptions { get; set; } = [];
    public List<string> EggOptions { get; set; } = [];
    public List<string> TimeSlots { get; set; } = [];
    public ProductOrderInput Order { get; set; } = new();
}
