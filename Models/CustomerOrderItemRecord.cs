using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class CustomerOrderItemRecord
{
    public long Id { get; set; }
    public long CustomerOrderRecordId { get; set; }

    [Required, StringLength(100)]
    public string ProductSlug { get; set; } = string.Empty;

    [Required, StringLength(120)]
    public string ProductName { get; set; } = string.Empty;

    [Required, StringLength(120)]
    public string ProductNameHindi { get; set; } = string.Empty;

    [Required, StringLength(500)]
    public string ImageUrl { get; set; } = string.Empty;

    public decimal UnitPrice { get; set; }
    public int Quantity { get; set; }

    [Required, StringLength(40)]
    public string Size { get; set; } = string.Empty;

    [Required, StringLength(40)]
    public string EggOption { get; set; } = string.Empty;

    [Required, StringLength(60)]
    public string City { get; set; } = string.Empty;

    [Required, StringLength(80)]
    public string Area { get; set; } = string.Empty;

    public DateTime DeliveryDate { get; set; }

    [Required, StringLength(50)]
    public string TimeSlot { get; set; } = string.Empty;

    [StringLength(40)]
    public string? Message { get; set; }
}
