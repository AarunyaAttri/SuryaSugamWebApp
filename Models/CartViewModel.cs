namespace WebApplication2.Models;

public sealed class CartViewModel
{
    public List<CartLineItem> Items { get; set; } = [];
    public int ItemCount => Items.Sum(item => item.Quantity);
    public decimal Subtotal => Items.Sum(item => item.UnitPrice * item.Quantity);
}
