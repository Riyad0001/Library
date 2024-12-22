from django.shortcuts import render
from .forms import UserRegisterForm
from django.contrib import messages
# Create your views here.
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .forms import DepositeMoneiForm
from book.models import BorrowHistory
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
def transaction_mail_send(user,subject,amount,template):
    message=render_to_string(template,{'user':user,'amount':amount})
    send_mail=EmailMultiAlternatives(subject,'',to=[user.email])
    send_mail.attach_alternative(message,"text/html")
    send_mail.send()

class SignUpView(CreateView):
  template_name = 'register.html'
  success_url = reverse_lazy('login')
  form_class = UserRegisterForm
  success_message = "Your profile was created successfully"
@login_required
def deposit_money(request):
    if request.method == 'POST':
        form = DepositeMoneiForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.balance += amount
            request.user.save()
            messages.success(request,f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully')
            transaction_mail_send(request.user,"Deposite Mail",amount,'deposite_email.html')
            return redirect('home')
    else:
        form = DepositeMoneiForm()
    return render(request, 'deposit_money.html', {'form': form})
@login_required
def user_profile(request):
    borrowing_history = BorrowHistory.objects.filter(user=request.user).order_by('-borrow_date')

    return render(request, 'user_profile.html', {
        'borrowing_history': borrowing_history,
    })


