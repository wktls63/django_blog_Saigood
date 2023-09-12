from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, TopicViewSet
from .views import signup

router = DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"topics", TopicViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('signup/', signup, name='signup'),
    # path('login/', login_view, name='login'),
]
