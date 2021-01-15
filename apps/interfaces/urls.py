from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"interfaces", views.InterfacesViewSet)

urlpatterns = [
]

urlpatterns += router.urls
