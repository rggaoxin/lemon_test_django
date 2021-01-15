from django.urls import path
from rest_framework import routers

from .views import DebugTalksViewSet

router = routers.DefaultRouter()
router.register(r'debugtalks', DebugTalksViewSet)

urlpatterns = [

]
urlpatterns += router.urls
