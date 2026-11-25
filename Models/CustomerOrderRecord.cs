using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class CustomerOrderRecord
{
    public long Id { get; set; }

    [Required, StringLength(32)]
    public string CustomerId { get; set; } = string.Empty;

    [Required, StringLength(2)]
    public string Language { get; set; } = "en";

    public decimal Subtotal { get; set; }
    public DateTimeOffset CreatedAt { get; set; } = DateTimeOffset.UtcNow;
    public List<CustomerOrderItemRecord> Items { get; set; } = [];
}
