<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

class PingController extends AbstractController
{
    #[Route('/mailer/ping', name: 'ping')]
    public function index(): Response
    {
        $textResponse = "pong";

        return new Response($textResponse, Response::HTTP_OK, ['Content-Type' => 'text/plain']);
    }
}
