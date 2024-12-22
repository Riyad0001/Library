from django.shortcuts import render
from book.models import Book,Review,Category
def home(request,catagory_slug=None):
    data=Book.objects.all()
    if catagory_slug is not None:
        category=Category.objects.get(slug=catagory_slug)
        data=Book.objects.filter(category=category)
    catagory=Category.objects.all()
    return render(request,'home.html',{'data':data,'catagory':catagory})
