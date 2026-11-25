namespace WebApplication2.Services;

public static class CustomerIdentity
{
    private const string CookieName = ".SuryaSugam.Customer";

    public static string GetOrCreate(HttpContext context)
    {
        if (context.Items.TryGetValue(CookieName, out var cached) && cached is string cachedId)
        {
            return cachedId;
        }

        if (context.Request.Cookies.TryGetValue(CookieName, out var existingId) && Guid.TryParseExact(existingId, "N", out _))
        {
            context.Items[CookieName] = existingId;
            return existingId;
        }

        var customerId = Guid.NewGuid().ToString("N");
        context.Items[CookieName] = customerId;

        if (!context.Response.HasStarted)
        {
            context.Response.Cookies.Append(CookieName, customerId, new CookieOptions
            {
                HttpOnly = true,
                IsEssential = true,
                SameSite = SameSiteMode.Lax,
                Secure = context.Request.IsHttps,
                MaxAge = TimeSpan.FromDays(365)
            });
        }

        return customerId;
    }
}
