from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.core.mail import EmailMessage
from rest_framework.views import APIView
from rest_framework.response import Response

class Sendmail(APIView):
    def post(self, request):
        email = request.data.get('email')
        subject = request.data.get('subject')
        body = request.data.get('body')

        email_message = EmailMessage(
            subject,
            body,
            to=[email],
            from_email=settings.EMAIL_HOST_USER
        )
        email_message.send()
        return Response({'message': 'Email sent successfully'})