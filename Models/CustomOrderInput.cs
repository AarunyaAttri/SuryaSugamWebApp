using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class CustomOrderInput
{
    [Required, StringLength(60, MinimumLength = 1)]
    public string CustomerName { get; set; } = string.Empty;

    [Required, Phone, StringLength(20, MinimumLength = 7)]
    public string Phone { get; set; } = string.Empty;

    [Required, StringLength(60, MinimumLength = 1)]
    public string Product { get; set; } = string.Empty;

    [Range(1, 500)]
    public int Quantity { get; set; } = 1;

    [StringLength(80)]
    public string? Occasion { get; set; }

    [DataType(DataType.Date)]
    public DateTime? PreferredDate { get; set; }

    [Required, StringLength(1000, MinimumLength = 1)]
    public string Details { get; set; } = string.Empty;

    [StringLength(2)]
    public string Language { get; set; } = "en";
}
