# Build stage
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src

# Restore dependencies first for better layer caching
COPY ["WebApplication2.csproj", "./"]
RUN dotnet restore "WebApplication2.csproj"

# Copy remaining source files and publish
COPY . .
RUN dotnet publish "WebApplication2.csproj" -c Release -o /app/publish /p:UseAppHost=false

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /app

ENV ASPNETCORE_URLS=http://+:8080
EXPOSE 8080

RUN mkdir -p /app/App_Data
COPY --from=build /app/publish .
ENTRYPOINT ["dotnet", "WebApplication2.dll"]
