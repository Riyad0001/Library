from django.urls import path,include
from .views import BookDetails,borrow_book,return_book,BookDetailsWithReview
urlpatterns = [
    path('book_detail/<int:id>',BookDetails.as_view(),name="book_detail"),
    path('book_detail_with_review/<int:id>',BookDetailsWithReview.as_view(),name="book_detail_with_review"),
    path('borrow_book/<int:book_id>',borrow_book,name="borrow_book"),
    path('return_book/<int:ret_id>',return_book,name="return_book"),
]