from rest_framework import routers

from .views import TestsuitsViewSet

router = routers.DefaultRouter()
router.register(r'testsuits', TestsuitsViewSet)

urlpatterns = [

]
urlpatterns += router.urls
