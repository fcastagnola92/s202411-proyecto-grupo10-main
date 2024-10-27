using delivery_together_offer_api.Context;
using delivery_together_offer_api.Contracts;
using delivery_together_offer_api.Dtos.Request;
using delivery_together_offer_api.Dtos.Response;
using delivery_together_offer_api.Enums;
using delivery_together_offer_api.Exceptions;
using delivery_together_offer_api.Models;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using RestSharp;
using System;
using System.Drawing;
using System.Net;

namespace delivery_together_offer_api.Business
{
    public class OfferService : IOfferService
    {
        private readonly OfferContext _context;

        public OfferService(OfferContext context)
        {
            _context = context;
        }

        public OfferResponse_Dto CreateOffer(string userId, Offer_Dto offer_Dto)
        {
            // Validar que los campos del DTO tienen el formato esperado
            if (string.IsNullOrEmpty(offer_Dto.Description))
            {
                throw new InvalidFieldsException("Los campos de la solicitud no tienen el formato esperado.");
            }

            // Validar que el tamaño del paquete sea válido
            if (offer_Dto.Size != PackageSize.SMALL.ToString() && offer_Dto.Size != PackageSize.MEDIUM.ToString() && offer_Dto.Size != PackageSize.LARGE.ToString() || offer_Dto.Offer < 0)
            {
                throw new UnexpectedValuesException("El tamaño del paquete no es válido.");
            }

            Offer newOffer = new Offer();

            newOffer.id = Guid.NewGuid().ToString(); // Generar un nuevo identificador UUID
            newOffer.postid = offer_Dto.PostId;
            newOffer.userid = userId;
            newOffer.description = offer_Dto.Description;
            newOffer.size = offer_Dto.Size.ToString();
            newOffer.fragile = offer_Dto.Fragile;
            newOffer.offer = offer_Dto.Offer;
            newOffer.createdat = DateTime.UtcNow;

            _context.offer.Add(newOffer);
            _context.SaveChanges();

            return new OfferResponse_Dto
            {
                Id = newOffer.id,// = offerId, REEMPLAZAR 
                UserId = userId,
                CreatedAt = newOffer.createdat
            };
        }

        public IEnumerable<OfferInfo_Dto> GetFilteredOffers(string? postId, string? owner)
        {
            var query = _context.offer.AsQueryable();

            // Filtrar por postId si está presente
            if (!string.IsNullOrEmpty(postId))
            {
                query = query.Where(o => o.postid == postId);
            }

            // Filtrar por owner si está presente y no es "me"
            if (!string.IsNullOrEmpty(owner) && owner != "me")
            {
                query = query.Where(o => o.userid == owner);
            }

            // Obtener las ofertas filtradas
            var offers = query.Select(o => new OfferInfo_Dto
            {
                id = o.id,
                postId = o.postid,
                description = o.description,
                size = o.size.ToString(),
                fragile = o.fragile,
                offer = o.offer,
                createdAt = o.createdat,
                userId = o.userid
            }).ToList();

            return offers;
        }

        public OfferInfo_Dto? GetOfferById(string id)
        {
            // Validar que el ID tenga el formato correcto
            if (!Guid.TryParse(id, out Guid offerId))
            {
                throw new ArgumentException("El ID no es un valor string con formato uuid.");
            }

            // Buscar la oferta en la base de datos por su ID
            var offer = _context.offer.FirstOrDefault(o => o.id == id);

            // Si no se encontró la oferta, retornar null
            if (offer == null)
            {
                return null;
            }

            // Mapear la oferta a un DTO y retornarla
            return new OfferInfo_Dto
            {
                id = offer.id,
                postId = offer.postid,
                description = offer.description,
                size = offer.size,
                fragile = offer.fragile,
                offer = offer.offer,
                createdAt = offer.createdat,
                userId = offer.userid
            };
        }

        public void DeleteOfferById(string id)
        {
            // Validar que el ID tenga el formato correcto
            if (!Guid.TryParse(id, out Guid offerId))
            {
                throw new ArgumentException("El ID no es un valor string con formato uuid.");
            }

            // Buscar la oferta en la base de datos por su ID
            var offer = _context.offer.FirstOrDefault(o => o.id == id);

            // Si no se encontró la oferta, lanzar una excepción
            if (offer == null)
            {
                throw new KeyNotFoundException("La oferta con ese ID no existe.");
            }

            // Eliminar la oferta de la base de datos y guardar los cambios
            _context.offer.Remove(offer);
            _context.SaveChanges();
        }

        public void ResetDatabase()
        {
            try
            {
                // Eliminar todos los datos de la tabla Offers
                _context.offer.RemoveRange(_context.offer);
                _context.SaveChanges();
            }
            catch (Exception ex)
            {
                // Capturar cualquier excepción y relanzarla
                throw new Exception("Error al restablecer la base de datos.", ex);
            }
        }

        public RestResponse? ObtenerUserIdDesdeToken(string Token, string UrlUsers)
        {
            var client = new RestClient(UrlUsers);

            var request = new RestRequest($"/users/me", Method.Get);

            request.AddHeader("Content-Type", "application/json");
            request.AddHeader("Authorization", Token);

            var response = client.Execute(request);

            return response;
        }
    }
}