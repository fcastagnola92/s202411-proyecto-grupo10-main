using delivery_together_offer_api.Context;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc.Authorization;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using System.Text;
using Microsoft.Extensions.DependencyInjection.Extensions;
using delivery_together_offer_api.Contracts;
using delivery_together_offer_api.Business;

public class Program
{
    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        builder.WebHost.UseUrls("http://*:3003");

        builder.Services
       .AddAuthorization()
       .AddAuthentication(x =>
       {
           x.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
           x.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
       }).AddJwtBearer(x =>
       {
           x.RequireHttpsMetadata = false;
           x.SaveToken = true;
           x.TokenValidationParameters = new TokenValidationParameters
           {
               ValidateIssuerSigningKey = true,
               ValidateIssuer = false,
               ValidateAudience = false
           };
       });

        //Add services to the container.�
        builder.Services.AddControllers();
        builder.Services.AddCors(options => options.AddPolicy("AllowWebApp",
          builder => builder.AllowAnyOrigin()
          .AllowAnyHeader()
          .AllowAnyMethod())); // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen(c =>
        {
            c.SwaggerDoc("v1", new OpenApiInfo
            {
                Title = "API",
                Version = "v1"
            });
            c.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
            {
                Name = "Authorization",
                Type = SecuritySchemeType.ApiKey,
                Scheme = "Bearer",
                BearerFormat = "Bearer",
                In = ParameterLocation.Header,
                Description = "Bearer Authorization header"
            });
            c.AddSecurityRequirement(new OpenApiSecurityRequirement {
        {
          new OpenApiSecurityScheme {
            Reference = new OpenApiReference {
              Type = ReferenceType.SecurityScheme,
                Id = "Bearer"
            }
          },
          new string[] {}
        }
      });
        });

        // Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();
        builder.Services.TryAddSingleton<IHttpContextAccessor, HttpContextAccessor>();
        builder.Services.AddScoped<IOfferService, OfferService>();
        builder.Services.AddDbContext<OfferContext>(options => options.UseNpgsql(builder.Configuration.GetConnectionString("DbConnection")));

        var app = builder.Build();

        // Verificar y aplicar migraciones al iniciar la aplicaci�n
        using (var serviceScope = app.Services.GetRequiredService<IServiceScopeFactory>().CreateScope())
        {
            var dbContext = serviceScope.ServiceProvider.GetService<OfferContext>();
            dbContext.Database.Migrate();
        }

        // Configure the HTTP request pipeline.
        if (app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        app.UseCors("AllowWebApp");
        app.UseAuthentication();
        app.UseHttpLogging();
        app.UseHttpsRedirection();
        app.MapControllers();
        app.UseRouting();
        app.UseAuthorization();

        app.Run();
    }
}