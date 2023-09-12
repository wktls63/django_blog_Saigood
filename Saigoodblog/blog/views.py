from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Article, Topic
from .serializers import ArticleSerializer, TopicSerializer

# 로그인
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

''' 로그인 구현
def login_view(request):
    # POST 요청이면 폼 데이터를 처리한다.
    if request.method == 'POST':

        # 폼 인스턴스를 생성하고 요청으로 받은 데이터를 채운다 (binding??)
        form = AuthenticationForm(request, data=request.POST)
        
        # 폼이 유효한지 체크한다.
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['pw']
            user = authenticate(request, username=username, password=password)

            # 로그인 성공하면 board_admin 화면으로 간다.
            if user is not None:
                login(request, user)
                return redirect('board_admin')
    
    # POST 요청이 아닌 경우 로그인 화면 보여준다.
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})
'''