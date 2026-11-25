using System.ComponentModel.DataAnnotations;

namespace WebApplication2.Models;

public sealed class NewsletterInput
{
    [Required(ErrorMessage = "Please enter your email address.")]
    [EmailAddress(ErrorMessage = "Enter a valid email address.")]
    [StringLength(254)]
    [Display(Name = "Email address")]
    public string Email { get; set; } = string.Empty;
}
