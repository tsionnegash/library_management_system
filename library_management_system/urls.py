"""
URL configuration for library_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
# library_management_system/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from library_app import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin interface
    path('api/', include('library_app.urls')),  # API endpoints

    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token obtain view
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Token refresh view

    # Simple homepage that links to Admin and API
    path('', views.home, name='home'),

    # Custom redirects
    path('admin-redirect/', RedirectView.as_view(url='/admin/', permanent=False), name='admin-redirect'),
    path('api-redirect/', RedirectView.as_view(url='/api/', permanent=False), name='api-root'),
]

