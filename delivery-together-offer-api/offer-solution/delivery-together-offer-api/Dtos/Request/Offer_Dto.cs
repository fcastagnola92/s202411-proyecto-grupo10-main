using delivery_together_offer_api.Enums;

namespace delivery_together_offer_api.Dtos.Request
{
    public class Offer_Dto
    {
        public string? PostId { get; set; }
        public string? Description { get; set; }
        public string? Size { get; set; }
        public bool Fragile { get; set; }
        public decimal Offer { get; set; }
    }
}