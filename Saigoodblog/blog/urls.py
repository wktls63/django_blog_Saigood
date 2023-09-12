from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, TopicViewSet
from .views import signup, board, write
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r"articles", ArticleViewSet)
router.register(r"topics", TopicViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('board/', board, name='board'),
    path('write/', write, name='write'),
]
