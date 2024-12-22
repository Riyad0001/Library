from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .models import Review,Book,BorrowHistory
from django.views.generic import DetailView
from .forms import ReviewForm
from django.contrib import messages
from django.utils.timezone import now
from accounts.views import transaction_mail_send
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class BookDetails(DetailView):
    model=Book
    pk_url_kwarg = 'id'
    template_name='book_detail.html'

    def post(self,request,*args,**kwargs):
        review_form=ReviewForm(data=self.request.POST)
        book=self.get_object()
        existing_review = Review.objects.filter(book=book, email=review_form.data.get('email')).first()

        if existing_review:
            messages.error(request, "You have already submitted a review for this book.")
            return redirect(reverse('book_detail', kwargs={'id': book.id}))
        if review_form.is_valid():
            new_review=review_form.save(commit=False)
            new_review.book=book
            new_review.save()
            messages.success(request, "Your review has been submitted successfully.")
            return redirect(reverse('book_detail', kwargs={'id': book.id}))
        return self.get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        post=self.object
        comments=post.reviews.all()
        review_form=ReviewForm()

        context['comments']=comments
        context['reviews_form']=review_form
        return context
@login_required
def borrow_book(request, book_id):  
    book = get_object_or_404(Book, id=book_id)   
    if request.user.balance >= book.borrowing_price:  
        request.user.balance -= book.borrowing_price  
        request.user.save()  
        BorrowHistory.objects.create(  
            user=request.user,  
            book=book,  
            amount=book.borrowing_price  
        ) 
        messages.success(request, f'You successfully borrowed "{book.title}".') 
        transaction_mail_send(request.user,"Borrow Book Mail",request.user.balance,'borrow_email.html')
        return redirect('profile')  
    else:    
        messages.error(request, 'You do not have enough balance to borrow this book.')  
        return redirect('book_detail',id=book.id) 
@login_required
def return_book(request, ret_id):
    borrow_history = get_object_or_404(BorrowHistory, id=ret_id, user=request.user, is_returned=False)
    request.user.balance += borrow_history.amount
    request.user.save()
    borrow_history.return_date = now()
    borrow_history.is_returned = True
    borrow_history.save()

    messages.success(request, f"You have successfully returned the book '{borrow_history.book.title}'. ${borrow_history.amount} has been refunded to your account.")
    return redirect('profile')


class BookDetailsWithReview(DetailView,LoginRequiredMixin):
    model=Book
    pk_url_kwarg = 'id'
    template_name='book_detail_review.html'

    def post(self,request,*args,**kwargs):
        review_form=ReviewForm(data=self.request.POST)
        book=self.get_object()
        existing_review = Review.objects.filter(book=book, email=review_form.data.get('email')).first()

        if existing_review:
            messages.error(request, "You have already submitted a review for this book.")
            return redirect(reverse('book_detail', kwargs={'id': book.id}))
        if review_form.is_valid():
            new_review=review_form.save(commit=False)
            new_review.book=book
            new_review.save()
            messages.success(request, "Your review has been submitted successfully.")
            return redirect(reverse('book_detail', kwargs={'id': book.id}))
        return self.get(request,*args,**kwargs)

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        post=self.object
        comments=post.reviews.all()
        review_form=ReviewForm()

        context['comments']=comments
        context['reviews_form']=review_form
        return context