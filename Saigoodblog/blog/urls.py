from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, TopicViewSet
from .views import board, write

from .views import SignUpView, posting, logout_view, LoginView

router = DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"topics", TopicViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    path("post/<int:article_id>", views.post_detail, name="post"),
    path("signup/", SignUpView.as_view(), name="sign_up"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),

    path('board/', board, name='board'),
    path('write/', write, name='write'),
]
