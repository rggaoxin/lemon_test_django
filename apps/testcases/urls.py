from rest_framework import routers

from . import views

router = routers.SimpleRouter()

router.register(r"testcases", views.TestcasesViewSet)

urlpatterns = [
]

urlpatterns += router.urls
