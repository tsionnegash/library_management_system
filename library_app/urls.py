from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, UserViewSet, TransactionViewSet

router = DefaultRouter()

router.register(r'books', BookViewSet) 
router.register(r'users', UserViewSet) 
router.register(r'transactions', TransactionViewSet) 


urlpatterns = [
    path('', include(router.urls)),  
]
