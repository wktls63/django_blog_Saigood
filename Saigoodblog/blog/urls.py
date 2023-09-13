from django.urls import path
from .views import SignUpView, posting

urlpatterns = [
    path("post/", posting, name="posting"),
    path("signup/", SignUpView.as_view(), name="sign_up"),
]
