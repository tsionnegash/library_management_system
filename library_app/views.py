from rest_framework import viewsets
from .models import Book, LibraryUser, Transaction
from .serializers import BookSerializer, UserSerializer, TransactionSerializer
from django.http import HttpResponse
from django.urls import reverse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# Simple homepage view linking to admin and API root
def home(request):
    admin_url = reverse('admin:index')  # Reverse lookup for the admin URL
    api_url = '/api/'  # Direct URL path for API root
    return HttpResponse(f"""
        <h1>Welcome to the Library Management System API!</h1>
        <p><a href='{admin_url}'>Go to Admin Interface</a></p>
        <p><a href='{api_url}'>Go to API Root</a></p>
    """)

# Book ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()  # Fetch all books
    serializer_class = BookSerializer  # Use the BookSerializer

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = LibraryUser.objects.all()  # Fetch all users
    serializer_class = UserSerializer  # Use the UserSerializer

# Transaction ViewSet
class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    # Custom action for checking out a book
    @action(detail=False, methods=['post'], url_path='checkout', url_name='checkout')
    def checkout(self, request):
        user = request.user
        book_id = request.data.get('book')  # Get the book ID from the request
        try:
            book = Book.objects.get(id=book_id)  # Get the book object
            if book.copies_available > 0:
                # Check if the user has already checked out the book and not returned it
                existing_transaction = Transaction.objects.filter(user=user, book=book, return_date__isnull=True).first()
                if existing_transaction:
                    return Response({'message': 'You have already checked out this book.'}, status=status.HTTP_400_BAD_REQUEST)

                # Proceed with checkout
                Transaction.objects.create(user=user, book=book)  # Create the transaction
                book.copies_available -= 1  # Decrease the available copies
                book.save()
                return Response({'message': 'Book checked out successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

    # Custom action for returning a book
    @action(detail=False, methods=['post'], url_path='return', url_name='return')
    def return_book(self, request):
        user = request.user
        book_id = request.data.get('book')  # Get the book ID from the request
        try:
            # Find the active (unreturned) transaction for this user and book
            transaction = Transaction.objects.filter(user=user, book__id=book_id, return_date__isnull=True).first()
            if transaction:
                transaction.return_date = timezone.now()  # Set the return date to now
                transaction.save()  # Save the updated transaction
                transaction.book.copies_available += 1  # Increase the available copies of the book
                transaction.book.save()  # Save the book
                return Response({'message': 'Book returned successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'No active checkout found for this book.'}, status=status.HTTP_400_BAD_REQUEST)
        except Transaction.DoesNotExist:
            return Response({'message': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
