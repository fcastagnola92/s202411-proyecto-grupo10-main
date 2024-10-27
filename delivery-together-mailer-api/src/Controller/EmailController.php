<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Mailer\MailerInterface;
use Symfony\Component\Mime\Email;
use Symfony\Component\HttpFoundation\JsonResponse;

class EmailController extends AbstractController
{
    #[Route('/mail/send', name: 'send')]
    public function sendEmail(Request $request, MailerInterface $mailer): JsonResponse
    {
        $data = json_decode($request->getContent(), true);

        $email = (new Email())
            ->from('deliverytogether@gmail.com')
            ->to($data['to'])
            ->subject($data['subject'])
            ->text($data['message']);

        $mailer->send($email);

        return new JsonResponse(['message' => 'Email sent successfully'], 200);
    }
}
