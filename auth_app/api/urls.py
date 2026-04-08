"""URL routing for authentication endpoints."""

from django.urls import path

from .views import EmailCheckView, LoginView, LogoutView, RegisterView

urlpatterns = [
    path('registration/', RegisterView.as_view(), name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('email-check/', EmailCheckView.as_view(), name='email-check'),
]
