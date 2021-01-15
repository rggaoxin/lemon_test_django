from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r"reports", views.ReportsViewSet)

urlpatterns = [
]

urlpatterns += router.urls
