from .views import SignUpView,deposit_money,user_profile
from django.urls import path,include
from django.contrib.auth.views import LogoutView,LoginView
urlpatterns = [
    path('signup/',SignUpView.as_view(),name="signup"),
    path('logout/',LogoutView.as_view(next_page='home'),name="logout"),
    path('login/',LoginView.as_view(template_name="login.html",next_page='home'),name="login"),
    path('deposit/',deposit_money,name="deposit"),
    path('profile/',user_profile,name="profile"),
]