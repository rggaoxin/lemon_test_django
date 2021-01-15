from django.urls import path, re_path
from rest_framework_jwt.views import obtain_jwt_token

from . import views

urlpatterns = [
    path('login/', obtain_jwt_token),
    path('register/', views.RegisterView.as_view()),

    re_path(r'^(?P<username>\w{6,20})/count/$',
            views.UsernameValidateView.as_view(), name='check_username'),
    re_path(r'^(?P<email>[A-Za-z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9_-]+)/count/$',
            views.EmailValidateView.as_view(), name='check_email'),
]

