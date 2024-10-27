using delivery_together_offer_api.Enums;

namespace delivery_together_offer_api.Dtos.Response
{
    public class OfferInfo_Dto
    {
        public string? id { get; set; } // Identificador de la oferta
        public string? postId { get; set; } // Identificador de la publicación asociada a la oferta
        public string? description { get; set; } // Descripción del paquete a llevar
        public string? size { get; set; } // Tamaño del paquete (LARGE, MEDIUM, SMALL)
        public bool fragile { get; set; } // Indica si es un paquete delicado o no
        public decimal offer { get; set; } // Valor en dólares de la oferta
        public DateTime createdAt { get; set; } // Fecha y hora de creación de la oferta
        public string? userId { get; set; } // Identificador del usuario que realizó la oferta
    }
}
