using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class ProductCommentInput
{
    [StringLength(60, MinimumLength = 1)]
    public string CustomerName { get; set; } = string.Empty;

    [StringLength(500, MinimumLength = 1)]
    public string Text { get; set; } = string.Empty;
}
