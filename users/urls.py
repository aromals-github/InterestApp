# urls.py
from django.urls import path
from .apis import SignupView, LoginView, LogoutView

urlpatterns = [
    path('interest/signup/', SignupView.as_view(), name='signup'),
    path('interest/login/', LoginView.as_view(), name='login'),
    path('interest/logout/', LogoutView.as_view(), name='logout'),
]
