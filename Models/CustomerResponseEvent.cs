using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class CustomerResponseEvent
{
    public long Id { get; set; }

    [Required, StringLength(32)]
    public string CustomerId { get; set; } = string.Empty;

    [Required, StringLength(60)]
    public string EventType { get; set; } = string.Empty;

    [StringLength(100)]
    public string? ProductSlug { get; set; }

    [Required]
    public string ResponseJson { get; set; } = "{}";

    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
}
