from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Article, Topic
from .serializers import ArticleSerializer, TopicSerializer

# 회원가입, 로그인, 로그아웃
from django.contrib.auth import authenticate, login
from .forms import UserForm


# Create your views here.
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        
        # 화면에서 입력한 데이터로 사용자 생성
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('board')
        
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form':form})

def board(request):
    return render(request, 'board.html')

def write(request):
    return render(request, 'write.html')