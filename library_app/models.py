from django.contrib.auth.models import AbstractUser
from django.db import models
class Book(models.Model):
    title = models.CharField(max_length=255)  
    author = models.CharField(max_length=255)  
    isbn = models.CharField(max_length=13, unique=True)  
    published_date = models.DateField() 
    copies_available = models.PositiveIntegerField(default=1) 

    def __str__(self):
        return self.title  


class LibraryUser(AbstractUser): 
    date_of_membership = models.DateField(auto_now_add=True) 
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.username  

class Transaction(models.Model):
    user = models.ForeignKey('LibraryUser', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    checkout_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} checked out {self.book.title}'

