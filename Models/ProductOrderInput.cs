using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class ProductOrderInput
{
    [Required]
    [StringLength(60)]
    [Display(Name = "City")]
    public string City { get; set; } = string.Empty;

    [Required]
    [StringLength(80)]
    [Display(Name = "Area")]
    public string Area { get; set; } = string.Empty;

    [Required]
    [DataType(DataType.Date)]
    [Display(Name = "Delivery date")]
    public DateTime? DeliveryDate { get; set; }

    [Required]
    [Display(Name = "Time slot")]
    public string TimeSlot { get; set; } = string.Empty;

    [Required]
    [Display(Name = "Size")]
    public string Size { get; set; } = "250 g";

    [Required]
    [Display(Name = "Egg option")]
    public string EggOption { get; set; } = "Eggless";

    [Range(1, 20, ErrorMessage = "Choose a quantity between 1 and 20.")]
    public int Quantity { get; set; } = 1;

    [StringLength(40, ErrorMessage = "The message can be at most 40 characters.")]
    [Display(Name = "Message (optional)")]
    public string? Message { get; set; }
}
