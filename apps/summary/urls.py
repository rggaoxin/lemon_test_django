from django.urls import path

from .views import SummaryAPIView

urlpatterns = [
    path('summary/', SummaryAPIView.as_view(), name='summary'),
]
