using delivery_together_offer_api.Dtos.Request;
using delivery_together_offer_api.Dtos.Response;
using RestSharp;

namespace delivery_together_offer_api.Contracts
{
    public interface IOfferService
    {
        OfferResponse_Dto CreateOffer(string userId, Offer_Dto offer_Dto);

        IEnumerable<OfferInfo_Dto> GetFilteredOffers(string? postId, string? owner);

        OfferInfo_Dto? GetOfferById(string id);

        void DeleteOfferById(string id);

        void ResetDatabase();

        RestResponse? ObtenerUserIdDesdeToken(string Token, string UrlUsers);
    }
}
