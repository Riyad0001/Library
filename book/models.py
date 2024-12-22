from django.db import models
from django.utils.text import slugify
from accounts.models import User
from django.utils import timezone
# Create your models here.

class Category(models.Model):  
    name = models.CharField(max_length=100)
    slug=models.SlugField(max_length=100,blank=True,null=True,unique=True)

    def __str__(self):
        return self.name


class Book(models.Model): 
    title = models.CharField(max_length=80)
    description = models.TextField()
    borrowing_price=models.IntegerField(blank=True,null=True)
    category = models.ManyToManyField(Category)  
    image = models.ImageField(upload_to="book/medias/uploads/", blank=True, null=True)
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title'] 


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=40)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.name} on {self.book.title}"

    class Meta:
        ordering = ['-created_on']

class BorrowHistory(models.Model):
    user = models.ForeignKey(User, related_name='borrow_history', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='borrowed_by', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} borrowed {self.book.title}'
