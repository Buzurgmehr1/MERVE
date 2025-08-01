from django.urls import path
from .views import register_view, login_view, logout_view, confirm_email
import uuid
urlpatterns = [
    path('confirm-email/<uuid:token>', confirm_email, name= 'confirm_email'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
]
