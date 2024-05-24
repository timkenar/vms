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


# visitors/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Visitor
from django.db.models import Count, DateTimeField
from django.db.models.functions import Trunc
import datetime

# visitors/views.py
from rest_framework import viewsets
from .models import Visitor
from .serializers import VisitorSerializer

# class VisitorViewSet(viewsets.ModelViewSet):
#     queryset = Visitor.objects.all()
#     serializer_class = VisitorSerializer


@api_view(['GET'])

def visitor_statistics(request):
    today = datetime.date.today()
    total_visitors = Visitor.objects.count()
    today_visitors = Visitor.objects.filter(check_in__date=today).count()

    # Additional analytics if needed
    visitors_per_day = Visitor.objects.annotate(day=Trunc('check_in', 'day', output_field=DateTimeField())) \
                                      .values('day') \
                                      .annotate(count=Count('id')) \
                                      .order_by('day')

    data = {
        'total_visitors': total_visitors,
        'today_visitors': today_visitors,
        'visitors_per_day': list(visitors_per_day),
    }
    return Response(data)

#For qr code...


import qrcode
from io import BytesIO
from django.http import HttpResponse
from rest_framework.decorators import api_view

@api_view(['GET'])
def generate_qr_code(request):
    data = request.query_params.get('data', 'http://127.0.0.1:8000/meetings/1')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill="black", back_color="white")

    # Create a BytesIO buffer to hold the image data
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")
