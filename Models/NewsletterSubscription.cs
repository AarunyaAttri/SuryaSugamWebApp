using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class NewsletterSubscription
{
    public long Id { get; set; }

    [Required, StringLength(32)]
    public string CustomerId { get; set; } = string.Empty;

    [Required, EmailAddress, StringLength(254)]
    public string Email { get; set; } = string.Empty;

    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
}
