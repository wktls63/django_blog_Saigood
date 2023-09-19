from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet
from .views import board, write, article_list, post_detail, create_or_update_post, autocomplete

from .views import SignUpView, posting, logout_view, LoginView

router = DefaultRouter()
router.register(r"articles", ArticleViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    
    path("signup/", SignUpView.as_view(), name="sign_up"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),

    path('board/', article_list, name='board'),
    path('board/<str:topic>', article_list, name='board_by_topic'),
    path("post/<int:article_id>", post_detail, name="posting"),
    path('write/', create_or_update_post, name='create_or_update_post'),
    path('edit_post/<int:post_id>/', create_or_update_post, name='create_or_update_post'),
    path('autocomplete/', autocomplete, name='autocomplete')
]
