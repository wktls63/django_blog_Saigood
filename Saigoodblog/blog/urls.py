from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, TopicViewSet
from .views import board, write
from django.contrib.auth import views as auth_views
from .views import SignUpView, posting, logout_view

router = DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"topics", TopicViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    path("post/", posting, name="posting"),
    path("signup/", SignUpView.as_view(), name="sign_up"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("logout/", logout_view, name="logout"),

    path('board/', board, name='board'),
    path('write/', write, name='write'),
]
