# SuryaSugam Bakery

ASP.NET Core MVC storefront for SuryaSugam Bakery.

## Run locally

Requires the .NET 10 SDK.

```powershell
dotnet restore
dotnet run --project .\WebApplication2.csproj
```

The app creates its SQLite database at `App_Data/suryasugam.db` on startup. Override the location with the `Database:Path` configuration setting. Local database files and environment files are excluded from Git.

## Included features

- Product catalog, cart, and checkout
- Custom bakery order requests and newsletter signups
- Product comments with live updates
- English and Hindi interface
- SQLite persistence for customer submissions and selections
