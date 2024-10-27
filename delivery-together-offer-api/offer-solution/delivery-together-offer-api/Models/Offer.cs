namespace delivery_together_offer_api.Models
{
    public class Offer
    {
        public string? id { get; set; } // Identificador de la oferta en formato uuid 4
        public string? postid { get; set; } // Identificador de la publicación asociada a la oferta
        public string? userid { get; set; } // Identificador del usuario que realizó la oferta
        public string? description { get; set; } // Descripción de no más de 140 caracteres sobre el paquete a llevar
        public string? size { get; set; } // Valor que describe subjetivamente del tamaño del paquete (LARGE, MEDIUM, SMALL)
        public bool fragile { get; set; } // Indica si es un paquete delicado o no
        public decimal offer { get; set; } // Valor en dólares de la oferta por llevar el paquete
        public DateTime createdat { get; set; }
    }
}
