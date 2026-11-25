using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class ProductComment
{
    public string Id { get; set; } = Guid.NewGuid().ToString("N");
    public string ProductSlug { get; set; } = string.Empty;
    [StringLength(60, MinimumLength = 1)]
    public string CustomerName { get; set; } = string.Empty;
    [StringLength(500, MinimumLength = 1)]
    public string Text { get; set; } = string.Empty;
    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
}
