using delivery_together_offer_api.Models;
using Microsoft.EntityFrameworkCore;

namespace delivery_together_offer_api.Context
{
    public class OfferContext : DbContext
    {
        public OfferContext(DbContextOptions<OfferContext> options) : base(options) { }

        public DbSet<Offer> offer { get; set; }
    }
}
