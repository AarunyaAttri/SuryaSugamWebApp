using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class CustomOrderRequestRecord
{
    public long Id { get; set; }

    [Required, StringLength(32)]
    public string CustomerId { get; set; } = string.Empty;

    [Required, StringLength(60)]
    public string CustomerName { get; set; } = string.Empty;

    [Required, StringLength(20)]
    public string Phone { get; set; } = string.Empty;

    [Required, StringLength(60)]
    public string Product { get; set; } = string.Empty;

    public int Quantity { get; set; }

    [StringLength(80)]
    public string? Occasion { get; set; }

    public DateTime? PreferredDate { get; set; }

    [Required, StringLength(1000)]
    public string Details { get; set; } = string.Empty;

    [Required, StringLength(2)]
    public string Language { get; set; } = "en";

    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
}
