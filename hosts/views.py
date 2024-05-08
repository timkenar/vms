import os
from io import BytesIO
from django.core.mail import EmailMessage, send_mail
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from .models import Host, Meeting
from .serializers import HostSerializer, MeetingSerializer, VisitorIDCardSerializer
from django.conf import settings
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist


from .id_card_generator import VisitorIDCardGenerator




class HostViewSet(viewsets.ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    parser_classes = [MultiPartParser]  # Add MultiPartParser to handle file uploads

    def perform_create(self, serializer):
        instance = serializer.save()

        # Send email to host
        host_email = instance.host.host_email
        host_subject = "New Visitor Details"
        host_message = f"Visitor Name: {instance.visitor_name}\nVisitor Email: {instance.visitor_email}\nVisitor Phone: {instance.visitor_phone}"

        image_path = os.path.join(settings.MEDIA_ROOT, str(instance.visitor_image))

        if os.path.exists(image_path):
            email = EmailMessage(
                host_subject,
                host_message,
                settings.EMAIL_HOST_USER,
                [host_email],
            )
            email.attach_file(image_path)
            email.send()

        # Send email to visitor
        visitor_email = instance.visitor_email
        visitor_subject = "Meeting Confirmation"
        visitor_message = f"Dear {instance.visitor_name},\n\nYour meeting details have been successfully submitted.\n\nHost Name: {instance.host.host_name}\nDate: {instance.date}\nTime In: {instance.time_in}\nTime Out: {instance.time_out or 'Not specified'}\n\nThank you."
        send_mail(visitor_subject, visitor_message, settings.EMAIL_HOST_USER, [visitor_email])

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class VisitorIDCardView(RetrieveAPIView):
    serializer_class = VisitorIDCardSerializer
    queryset = Meeting.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            visitor_name = instance.visitor_name
            
            # Ensure the visitor image path exists
            if instance.visitor_image:
                # Read the visitor image file and get binary data
                with open(instance.visitor_image.path, "rb") as f:
                    visitor_image_data = f.read()
            else:
                return Response({'error': 'Visitor image path does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Generate ID card PNG
            id_card_buffer = VisitorIDCardGenerator.generate(visitor_name=visitor_name, visitor_image_data=visitor_image_data)

            # Return ID card PNG in response
            return HttpResponse(id_card_buffer.getvalue(), content_type='image/png')

        except ObjectDoesNotExist:
            return Response({'error': 'Meeting object does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class VisitorIDCardView(RetrieveAPIView):
#     serializer_class = VisitorIDCardSerializer
#     queryset = Meeting.objects.all()

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         visitor_image_url = request.build_absolute_uri(instance.visitor_image.url)  # Use url instead of path
#         serializer = self.get_serializer(instance)
#         id_card_data = serializer.data

#         try:
#             id_card_buffer = VisitorIDCardGenerator.generate(visitor_name=id_card_data['visitor_name'], visitor_image_path=visitor_image_url)
#         except IOError as e:
#             return Response({'error': 'Failed to generate ID card.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         return Response({'id_card': id_card_buffer.getvalue()}, status=status.HTTP_200_OK)

# class VisitorIDCardViewSet(RetrieveAPIView):
#     serializer_class = VisitorIDCardSerializer
#     queryset = Meeting.objects.all()

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         id_card_data = serializer.save()
#         return Response(id_card_data, status=status.HTTP_200_OK)

# class VisitorIDCardViewSet(viewsets.ViewSet):
#     serializer_class = VisitorIDCardSerializer

#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             id_card_data = serializer.save()
#             return Response(id_card_data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)