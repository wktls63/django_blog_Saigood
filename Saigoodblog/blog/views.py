from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from .models import Article, Topic
from .serializers import ArticleSerializer, TopicSerializer
from .forms import SignUpForm, LoginForm, BlogPostForm
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView
from django.utils.decorators import method_decorator

# 글 생성
def modelForm(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('board')
    else:
        form = BlogPostForm()
    return render(request, 'write.html', {'form':form})

# 글 목록 띄우기
def article_list(request):
    # 블로그 글들을 모조리 띄우는 코드
    # posts = Article.objects.all()
    # 최신글 정렬
    posts = Article.objects.filter().order_by('-posted_date')
    return render(request, 'post.html', {'posts': posts})


# 포스트 업로드, 업데이트, 삭제
# def create_or_update_post(request, post_id=None):
#     # 글 수정
#     if post_id:
#         post = get_object_or_404(Article, id=post_id)

#     # 글 작성
#     else:
#         post = Article.objects.filter(article_id=request.user.username, publish='N').order_by('-posted_date').first()

#     if request.method == 'POST':
#         form = BlogPostForm(request.POST, instance=post) # 폼 초기화

#         # 삭제
#         if 'delete-btn' in request.POST:
#             post.delete()
#             return redirect('post')

#         if not form.cleaned_data.get('topic'):
#             post.topic = '전체'

#         # 임시저장
#         if '' in request.POST:
#             post.publish = 'N'
#         else:
#             post.publish = 'Y'

#         # 작성자
#         post.article_id = request.user.username

#         post.save()
#         return redirect('post', post_id=post.id)

#     else:
#         form = BlogPostForm(instance=post)


# 회원가입, 로그인, 로그아웃


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


def board(request):
    return render(request, 'board.html')

def write(request):
    return render(request, 'write.html')



def my_decorator(function):
    def decorator_func(request):
        if not request.user.is_anonymous:
            return redirect("posting")
        return function(request)

    return decorator_func

def posting(request):
    return render(request, "post.html")

# 로그아웃 (화면없이 기능 동작 후, 리다이렉트)
def logout_view(request):
    logout(request)
    return redirect("sign_up")


@method_decorator(my_decorator, name="get")
class SignUpView(FormView):
    template_name = "sign_up.html"
    form_class = SignUpForm
    success_url = "/blog/post/"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        print("SignUpView - form_valid")
        # User
        email = form.data.get("email")
        password = form.data.get("password")


        # 유저 생성
        user = User.objects.create_user(email, password)

        # 회원가입 인증 후, 바로 로그인 처리
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("SignUpView - form_invalid")
        return super().form_invalid(form)
    

@method_decorator(my_decorator, name="get")
class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm
    success_url = "/blog/board/"
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form):
        email = form.data.get("email")
        password = form.data.get("password")
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)