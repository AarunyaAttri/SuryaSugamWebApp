namespace WebApplication2.Models;

public sealed class NavigationLink
{
    public string Label { get; set; } = string.Empty;
    public string Url { get; set; } = "#";
    public List<NavigationLink> Children { get; set; } = [];
}
