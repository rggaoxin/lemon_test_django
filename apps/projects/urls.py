from rest_framework import routers

from . import views

# 1. 创建SimpleRouter路由对象
router = routers.SimpleRouter()
# 使用DefaultRouter, 会自动创建根路由页面
# router = routers.DefaultRouter()

# 2. 注册路由
# 第一个参数为prefix路由前缀(支持正则表达式), 一般添加为应用名即可
# 第二个参数为视图集类(只有视图集类才能支持router)
# 第三个参数为basename, 指定url别名前缀
# router.register(r"projects", views.ProjectViewSet, basename="bs")
router.register(r"projects", views.ProjectViewSet)

# 子路由(子应用下创建的路由表)
urlpatterns = [
]

# 4. 或者将url添加到urlpatterns列表中
urlpatterns += router.urls
