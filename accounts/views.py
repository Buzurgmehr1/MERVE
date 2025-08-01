from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import login, logout, authenticate

from .helpers import send_confirmation_token
from .models import Token, CustomUser
# Create your views here.

def confirm_email(request, token):
    try:
        email_confirm_object = Token.objects.get(token=token)
    except Token.DoesNotExist:
        return HttpResponse('Token invalid or expired !')
    user = email_confirm_object.user
    user.is_active = True
    user.is_confirmed_email = True
    user.save()
    email_confirm_object.delete()
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', False)
        password = request.POST.get('password',False)
        confirm_password = request.POST.get('confirm_password', False)

        if CustomUser.objects.filter(email = email).exists():
            return HttpResponse('Email alredy exists. Please try to LOGIN.')
        if password != confirm_password:
            return HttpResponse("Passwords don't match")
        
        user = CustomUser.objects.create_user(
            email=email,
            password=password
        )
        user.is_active = False
        user.save()
        confirm_email_object = Token.objects.create(user=user)
        token = confirm_email_object.token
        res = send_confirmation_token(email, token)
        if res['is_sent']:
            return redirect('login')
        return HttpResponse("Error: Your data is saved but confirmation email failed to send.")
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email',False)
        password = request.POST.get('password',False)

        user = authenticate(request, email = email, password = password)
        if user is not None:
            if user.is_confirmed_email:
                login(request,user)
                return redirect('product_list')
            return HttpResponse('Your email is not confirmed please firs confirm email.')
        return HttpResponse('Invalid Cridentials')
    return render(request, 'accounts/login.html')
    
def logout_view(request):
    try:
        logout(request)
        return redirect('login')
    except Exception as ex:
        return HttpResponse('error' + str(ex))
    