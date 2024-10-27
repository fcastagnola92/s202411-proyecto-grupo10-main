using delivery_together_offer_api.Business;
using delivery_together_offer_api.Context;
using delivery_together_offer_api.Contracts;
using delivery_together_offer_api.Dtos.Request;
using delivery_together_offer_api.Models;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations;
using System.Net.Http.Headers;
using System.Net;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Http.HttpResults;
using delivery_together_offer_api.Exceptions;

namespace delivery_together_offer_api.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class OffersController : ControllerBase
    {
        private readonly OfferContext _context;
        private IOfferService _offerService;
        private readonly string _apiUsers;
        private string _authorizationHeader;
        private readonly IConfiguration _configuration;

        public OffersController(OfferContext context, IOfferService offerService, IConfiguration configuration)
        {
            _configuration = configuration;

            _apiUsers = !string.IsNullOrEmpty(Environment.GetEnvironmentVariable("USERS_PATH")) ? Environment.GetEnvironmentVariable("USERS_PATH") : _configuration["USERS_PATH"];
            _context = context;
            _offerService = offerService;
        }

        [HttpPost("/offers")]
        public IActionResult CreateOffer(Offer_Dto offers)
        {
            try
            {
                IActionResult result = CheckAuthorization();

                if (result is OkResult)
                {
                    var responseDTO = _offerService.CreateOffer(Guid.NewGuid().ToString(), offers);

                    return StatusCode(201, responseDTO);
                }
                else
                {
                    return result;
                }
            }
            catch (UnauthorizedAccessException)
            {
                return StatusCode(401, "El token no es válido o está vencido.");
            }
            catch (InvalidOperationException)
            {
                return StatusCode(403, "No hay token en la solicitud.");
            }
            catch (InvalidFieldsException ex)
            {
                return StatusCode(400, ex.Message);
            }
            catch (UnexpectedValuesException ex)
            {
                return StatusCode(412, ex.Message);
            }
            catch (Exception ex)
            {
                return StatusCode(500, "Ocurrió un error al procesar la solicitud." + ex.Message);
            }
        }

        [HttpGet("/offers/")]
        public IActionResult GetFilteredOffers(string? post, string? owner)
        {
            try
            {
                IActionResult result = CheckAuthorization();

                if (result is OkResult)
                {
                    // Obtener y filtrar las ofertas
                    var offersDTO = _offerService.GetFilteredOffers(post, owner);

                    return Ok(offersDTO);
                }
                else
                {
                    return result;
                }
            }
            catch (UnauthorizedAccessException)
            {
                return StatusCode(401, "El token no es válido o está vencido.");
            }
            catch (Exception ex)
            {
                return StatusCode(500, "Ocurrió un error al procesar la solicitud." + ex.Message);
            }
        }

        [HttpGet("/offers/{id}")]
        public IActionResult GetOfferById(string id)
        {
            try
            {
                IActionResult result = CheckAuthorization();

                if (result is OkResult)
                {
                    // Obtener la oferta por su ID
                    var offerDTO = _offerService.GetOfferById(id);

                    if (offerDTO == null)
                    {
                        return NotFound("La oferta con ese ID no existe.");
                    }

                    return Ok(offerDTO);
                }
                else
                {
                    return result;
                }
            }
            catch (UnauthorizedAccessException)
            {
                return StatusCode(401, "El token no es válido o está vencido.");
            }
            catch (ArgumentException ex)
            {
                return BadRequest(ex.Message);
            }
            catch (Exception ex)
            {
                return StatusCode(500, "Ocurrió un error al procesar la solicitud." + ex.Message);
            }
        }

        [HttpDelete("/offers/{id}")]
        public IActionResult DeleteOfferById(string id)
        {
            try
            {
                IActionResult result = CheckAuthorization();

                if (result is OkResult)
                {

                    // Eliminar la oferta por su ID
                    _offerService.DeleteOfferById(id);

                    // Retornar respuesta exitosa
                    return Ok(new { msg = "la oferta fue eliminada" });
                }
                else
                {
                    return result;
                }
            }
            catch (UnauthorizedAccessException)
            {
                return StatusCode(401, "El token no es válido o está vencido.");
            }
            catch (ArgumentException ex)
            {
                return BadRequest(ex.Message);
            }
            catch (KeyNotFoundException ex)
            {
                return NotFound(ex.Message);
            }
            catch (Exception ex)
            {
                return StatusCode(500, "Ocurrió un error al procesar la solicitud." + ex.Message);
            }
        }

        [HttpGet("/offers/ping")]
        public IActionResult Ping()
        {
            return Ok("pong");
        }

        [HttpPost("/offers/reset")]
        public IActionResult ResetDatabase()
        {
            try
            {
                // Llamar al método en el servicio para resetear la base de datos
                _offerService.ResetDatabase();

                // Retornar respuesta exitosa con mensaje
                return Ok(new { msg = "Todos los datos fueron eliminados." });
            }
            catch (Exception ex)
            {
                // Retornar código de error en caso de fallo
                return StatusCode(500, $"Ocurrió un error al restablecer la base de datos: {ex.Message}");
            }
        }

        public IActionResult CheckAuthorization()
        {
            _authorizationHeader = Request.Headers["Authorization"];

            if (string.IsNullOrEmpty(_authorizationHeader))
            {
                return StatusCode(403, "No hay token en la solicitud.");
            }

            var response = _offerService.ObtenerUserIdDesdeToken(_authorizationHeader, _apiUsers);

            if (response == null || response.StatusCode != HttpStatusCode.OK)
            {
                return StatusCode(401, "El token no es válido o está vencido.");
            }

            return Ok();
        }
    }
}
