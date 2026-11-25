using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class CartQuantityInput
{
    [Required]
    public string Id { get; set; } = string.Empty;

    [Range(1, 20, ErrorMessage = "Choose a quantity between 1 and 20.")]
    public int Quantity { get; set; } = 1;
}
