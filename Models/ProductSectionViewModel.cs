namespace WebApplication2.Models;

public sealed class ProductSectionViewModel
{
    public string Id { get; set; } = string.Empty;
    public string Eyebrow { get; set; } = string.Empty;
    public string EyebrowHindi { get; set; } = string.Empty;
    public string Title { get; set; } = string.Empty;
    public string TitleHindi { get; set; } = string.Empty;
    public string Description { get; set; } = string.Empty;
    public string DescriptionHindi { get; set; } = string.Empty;
    public string LinkLabel { get; set; } = string.Empty;
    public string LinkLabelHindi { get; set; } = string.Empty;
    public string LinkUrl { get; set; } = "#";
    public List<ProductCard> Products { get; set; } = [];
}
