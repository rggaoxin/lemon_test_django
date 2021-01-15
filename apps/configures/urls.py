from rest_framework import routers

from .views import ConfiguresViewSet

router = routers.DefaultRouter()
router.register(r'configures', ConfiguresViewSet)

urlpatterns = [

]
urlpatterns += router.urls
