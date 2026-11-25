using Microsoft.EntityFrameworkCore;
using WebApplication2.Models;

namespace WebApplication2.Data;

public sealed class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    public DbSet<CartLineItem> CartItems => Set<CartLineItem>();
    public DbSet<CustomerOrderRecord> CustomerOrders => Set<CustomerOrderRecord>();
    public DbSet<CustomerOrderItemRecord> CustomerOrderItems => Set<CustomerOrderItemRecord>();
    public DbSet<CustomOrderRequestRecord> CustomOrderRequests => Set<CustomOrderRequestRecord>();
    public DbSet<CustomerResponseEvent> CustomerResponseEvents => Set<CustomerResponseEvent>();
    public DbSet<NewsletterSubscription> NewsletterSubscriptions => Set<NewsletterSubscription>();
    public DbSet<ProductComment> ProductComments => Set<ProductComment>();

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<CartLineItem>().HasKey(item => item.Id);
        modelBuilder.Entity<CartLineItem>().HasIndex(item => new { item.CustomerId, item.Id });
        modelBuilder.Entity<CustomerOrderRecord>().HasIndex(order => new { order.CustomerId, order.CreatedAt });
        modelBuilder.Entity<CustomerOrderItemRecord>().HasOne<CustomerOrderRecord>().WithMany(order => order.Items).HasForeignKey(item => item.CustomerOrderRecordId).OnDelete(DeleteBehavior.Cascade);
        modelBuilder.Entity<CustomOrderRequestRecord>().HasIndex(request => new { request.CustomerId, request.CreatedAt });
        modelBuilder.Entity<CustomerResponseEvent>().HasIndex(response => new { response.CustomerId, response.CreatedAt });
        modelBuilder.Entity<NewsletterSubscription>().HasIndex(subscription => subscription.Email);
        modelBuilder.Entity<ProductComment>().HasIndex(comment => new { comment.ProductSlug, comment.CreatedAt });
    }
}
