using Microsoft.AspNetCore.DataProtection;
using Microsoft.AspNetCore.HttpOverrides;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;
using WebApplication2.Controllers;
using WebApplication2.Data;
using WebApplication2.Models;
using WebApplication2.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();
var configuredDatabasePath = builder.Configuration["Database:Path"];
if (string.IsNullOrWhiteSpace(configuredDatabasePath))
{
    var azureHome = Environment.GetEnvironmentVariable("HOME");
    var isAzureAppService = !string.IsNullOrWhiteSpace(Environment.GetEnvironmentVariable("WEBSITE_SITE_NAME"));
    configuredDatabasePath = isAzureAppService && !string.IsNullOrWhiteSpace(azureHome)
        ? Path.Combine(azureHome, "data", "suryasugam.db")
        : Path.Combine("App_Data", "suryasugam.db");
}
var databasePath = Path.IsPathRooted(configuredDatabasePath)
    ? configuredDatabasePath
    : Path.Combine(builder.Environment.ContentRootPath, configuredDatabasePath);
var appDataDirectory = Path.GetDirectoryName(databasePath) ?? Path.Combine(builder.Environment.ContentRootPath, "App_Data");
Directory.CreateDirectory(appDataDirectory);
var keysDirectory = Path.Combine(appDataDirectory, "keys");
Directory.CreateDirectory(keysDirectory);

builder.Services.AddDataProtection()
    .SetApplicationName("SuryaSugamBakery")
    .PersistKeysToFileSystem(new DirectoryInfo(keysDirectory));

builder.Services.Configure<ForwardedHeadersOptions>(options =>
{
    options.ForwardedHeaders = ForwardedHeaders.XForwardedFor | ForwardedHeaders.XForwardedProto;
    options.KnownIPNetworks.Clear();
    options.KnownProxies.Clear();
});

builder.Services.AddDbContext<AppDbContext>(options => options.UseSqlite($"Data Source={databasePath}"));
builder.Services.AddSingleton<ProductCommentStore>();

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var database = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    database.Database.EnsureCreated();
    database.Database.ExecuteSqlRaw("PRAGMA busy_timeout = 5000;");
}

app.UseForwardedHeaders();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

var hasHttpsConfigured = !string.IsNullOrWhiteSpace(builder.Configuration["HTTPS_PORTS"])
    || !string.IsNullOrWhiteSpace(builder.Configuration["ASPNETCORE_HTTPS_PORTS"])
    || (builder.Configuration["ASPNETCORE_URLS"]?.Contains("https://", StringComparison.OrdinalIgnoreCase) ?? false);
if (hasHttpsConfigured)
{
    app.UseHttpsRedirection();
}

app.UseRouting();
app.UseAuthorization();

app.MapStaticAssets();

app.MapGet("/health", async (AppDbContext database, CancellationToken cancellationToken) =>
{
    var canConnect = await database.Database.CanConnectAsync(cancellationToken);
    return canConnect
        ? Results.Ok(new { status = "healthy" })
        : Results.Problem("Database unavailable", statusCode: StatusCodes.Status503ServiceUnavailable);
});

app.MapGet("/products/{slug}/comments", async (string slug, AppDbContext database, CancellationToken cancellationToken) =>
{
    if (!IsValidProductSlug(slug))
    {
        return Results.BadRequest(new { message = "Invalid product." });
    }

    // Load matching comments and sort in memory because SQLite EF Core cannot translate ORDER BY on DateTimeOffset.
    var comments = await database.ProductComments
        .AsNoTracking()
        .Where(comment => comment.ProductSlug == slug)
        .ToListAsync(cancellationToken);

    var recentComments = comments
        .OrderBy(comment => comment.CreatedAt)
        .TakeLast(100);

    return Results.Json(recentComments);
});

app.MapPost("/products/{slug}/comments", async (string slug, ProductCommentInput input, AppDbContext database, ProductCommentStore comments, HttpContext context) =>
{
    if (!IsValidProductSlug(slug))
    {
        return Results.BadRequest(new { message = "Invalid product." });
    }

    var name = input.CustomerName?.Trim();
    var text = input.Text?.Trim();
    if (string.IsNullOrWhiteSpace(name) || name.Length > 60 || string.IsNullOrWhiteSpace(text) || text.Length > 500)
    {
        return Results.BadRequest(new { message = "Enter your name and a comment of up to 500 characters." });
    }

    var comment = new ProductComment
    {
        ProductSlug = slug,
        CustomerName = name,
        Text = text
    };
    database.ProductComments.Add(comment);
    database.CustomerResponseEvents.Add(new CustomerResponseEvent
    {
        CustomerId = CustomerIdentity.GetOrCreate(context),
        EventType = "ProductCommentSubmitted",
        ProductSlug = slug,
        ResponseJson = JsonSerializer.Serialize(new { comment.CustomerName, comment.Text })
    });
    await database.SaveChangesAsync(context.RequestAborted);
    comments.PublishComment(comment);

    return Results.Ok(comment);
});

app.MapGet("/products/{slug}/comments/live", async (string slug, HttpContext context, ProductCommentStore comments) =>
{
    if (!IsValidProductSlug(slug))
    {
        context.Response.StatusCode = StatusCodes.Status400BadRequest;
        return;
    }

    context.Response.Headers.ContentType = "text/event-stream";
    context.Response.Headers.CacheControl = "no-cache";
    context.Response.Headers.Append("X-Accel-Buffering", "no");
    var subscription = comments.Subscribe(slug);
    try
    {
        await context.Response.WriteAsync(": connected\n\n", context.RequestAborted);
        await context.Response.Body.FlushAsync(context.RequestAborted);

        while (!context.RequestAborted.IsCancellationRequested)
        {
            using var keepaliveCts = CancellationTokenSource.CreateLinkedTokenSource(context.RequestAborted);
            keepaliveCts.CancelAfter(TimeSpan.FromSeconds(25));

            bool hasData;
            try
            {
                hasData = await subscription.Reader.WaitToReadAsync(keepaliveCts.Token);
            }
            catch (OperationCanceledException) when (!context.RequestAborted.IsCancellationRequested)
            {
                await context.Response.WriteAsync(": keepalive\n\n", context.RequestAborted);
                await context.Response.Body.FlushAsync(context.RequestAborted);
                continue;
            }

            if (!hasData)
            {
                break;
            }

            while (subscription.Reader.TryRead(out var comment))
            {
                await context.Response.WriteAsync($"data: {JsonSerializer.Serialize(comment)}\n\n", context.RequestAborted);
                await context.Response.Body.FlushAsync(context.RequestAborted);
            }
        }
    }
    catch (OperationCanceledException)
    {
    }
    finally
    {
        comments.Unsubscribe(slug, subscription.Id);
    }
});

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}")
    .WithStaticAssets();

app.Run();

static bool IsValidProductSlug(string slug) =>
    !string.IsNullOrWhiteSpace(slug)
    && slug.Length is >= 1 and <= 100
    && System.Text.RegularExpressions.Regex.IsMatch(slug, "^[a-z0-9-]+$")
    && HomeController.IsKnownProductSlug(slug);
