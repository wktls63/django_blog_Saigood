from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets
from .models import Article
from .serializers import ArticleSerializer
from .forms import SignUpForm, LoginForm, BlogPostForm
from .models import User
from django.contrib.auth import login, logout, authenticate
from django.views.generic import FormView
from django.utils.decorators import method_decorator
from bs4 import BeautifulSoup
from django.conf import settings


from bs4 import BeautifulSoup
from django.conf import settings

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

def post_detail(request, article_id):
    # article_id로 게시글 가져오기
    # post = Article.objects.get(article_id=article_id)
    post = get_object_or_404(Article, article_id=article_id)

    # 조회수 증가 및 db에 저장
    post.views += 1 
    post.save()

    # 이전/다음 게시물 가져옴
    prev_post = Article.objects.filter(article_id__lt=post.article_id, publish='Y').order_by('-article_id').first()
    next_post = Article.objects.filter(article_id__gt=post.article_id, publish='Y').order_by('article_id').first()

    # 같은 주제인 게시물들 중 최신 글 가져옴
    recommended_posts = Article.objects.filter(topic=post.topic, publish='Y').exclude(article_id=post.article_id).order_by('-updated_date')[:2]

    # 게시물 내용에서 첫번째 이미지(썸네일) 태그 추출
    for recommended_post in recommended_posts:
        soup = BeautifulSoup(recommended_post.content, 'html.parser')
        image_tag = soup.find('img')
        recommended_post.image_tag = str(image_tag) if image_tag else ''
    
    context = {
        'post': post,
        'prev_post': prev_post,
        'next_post': next_post,
        'recommended_posts': recommended_posts,
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, 'post.html', context)


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




# def post_detail(request, article_id):
#     # article_id로 게시글 가져오기
#     # post = Article.objects.get(article_id=article_id)
#     post = get_object_or_404(Article, article_id=article_id)

#     # 조회수 증가 및 db에 저장
#     post.views += 1 
#     post.save()

#     # 이전/다음 게시물 가져옴
#     prev_post = Article.objects.filter(article_id__lt=post.article_id, publish='Y').order_by('-article_id').first()
#     next_post = Article.objects.filter(article_id__gt=post.article_id, publish='Y').order_by('article_id').first()

#     # 같은 주제인 게시물들 중 최신 글 가져옴
#     recommended_posts = Article.objects.filter(topic=post.topic, publish='Y').exclude(article_id=post.article_id).order_by('-updated_date')[:2]

#     # 게시물 내용에서 첫번째 이미지(썸네일) 태그 추출
#     for recommended_post in recommended_posts:
#         soup = BeautifulSoup(recommended_post.content, 'html.parser')
#         image_tag = soup.find('img')
#         recommended_post.image_tag = str(image_tag) if image_tag else ''
    
#     context = {
#         'post': post,
#         'prev_post': prev_post,
#         'next_post': next_post,
#         'recommended_posts': recommended_posts,
#         'MEDIA_URL': settings.MEDIA_URL,
#     }

#     return render(request, 'post.html', context)



# 글 목록 띄우기
def article_list(request, topic=None):
    
    # 선택된 주제 있을 경우 필터링
    if topic:
        posts = Article.objects.filter(topic=topic, publish='Y').order_by('-views')

    # 선택된 주제 없을 경우 모든 글목록 보여줌
    else:
        posts = Article.objects.filter(publish='Y').order_by('-views')

    # 조회수가 가장 
    top_post = posts.first()

    return render(request, 'board.html', {'posts':posts, 'top_post':top_post})



def create_or_update_post(request, post_id=None):
    # 글수정 페이지의 경우
    if post_id:
        post = get_object_or_404(Article, id=post_id)
    
    # 글쓰기 페이지의 경우, 임시저장한 글이 있는지 검색 
    else:
        post = Article.objects.filter(article_id=request.user.id, publish='N').order_by('-updated_date').first()

    # 업로드/수정 버튼 눌렀을 떄
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post) # 폼 초기화
        if form.is_valid():
            post = form.save(commit=False)

            # 게시물 삭제
            if 'delete-button' in request.POST:
                post.delete() 
                return redirect('board') 

            if not form.cleaned_data.get('topic'):
                post.topic = '전체'
            
            # 임시저장 여부 설정
            if 'temp-save-button' in request.POST:
                post.publish = 'N'
            else:
                post.publish = 'Y'

            # 글쓴이 설정
            post.author_id = request.user.username

            post.save()
            return redirect('post.html', post_id=post.id) # 업로드/수정한 페이지로 리다이렉트
    
    # 수정할 게시물 정보를 가지고 있는 객체를 사용해 폼을 초기화함
    else:
        form = BlogPostForm(instance=post)

    template = 'write.html'
    context = {'form': form, 'post': post, 'edit_mode': post_id is not None, 'MEDIA_URL': settings.MEDIA_URL,} #edit_mode: 글 수정 모드여부

    return render(request, template, context)




class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer



def board(request):
    return render(request, 'board.html')

def write(request):
    return render(request, 'write.html')



def my_decorator(function):
    def decorator_func(request):
        if not request.user.is_anonymous:
            return redirect("board")
        return function(request)

    return decorator_func

def posting(request):
    return render(request, "post.html")

# 로그아웃 (화면없이 기능 동작 후, 리다이렉트)
def logout_view(request):
    logout(request)
    return redirect("login")


@method_decorator(my_decorator, name="get")
class SignUpView(FormView):
    template_name = "sign_up.html"
    form_class = SignUpForm
    success_url = "/blog/board/"

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