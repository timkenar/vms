"""
URL configuration for email_me project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from hosts.views import *
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'hosts', HostViewSet)
router.register(r'meetings', MeetingViewSet)
# router.register(r'visitors', VisitorViewSet)
# router.register(r'accounts', CustomUser)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate-id-card/<int:pk>/', VisitorIDCardView.as_view(), name = 'generate_id_card'),
    path('api/', include('accounts.urls')),
    path('', include('send.urls')),
    path('', include(router.urls)),
    path('analytics/', visitor_statistics, name='visitor_statistics'),
    path('generate_qr_code/', generate_qr_code, name='generate_qr_code'),
    
]

urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


