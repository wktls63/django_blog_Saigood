from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from ckeditor_uploader.fields import RichTextUploadingField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.save(using=self._db)
        return user


class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="생성일", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="갱신일", auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel, AbstractBaseUser):
    email = models.EmailField(verbose_name="이메일", max_length=100, unique=True)
    password = models.CharField(verbose_name="비밀번호", max_length=255)
    is_active = models.BooleanField(verbose_name="활성 여부", default=True)
    is_staff = models.BooleanField(verbose_name="관리자 여부", default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"


class Article(models.Model):
    article_id                  = models.AutoField(primary_key = True, verbose_name = "게시글ID")
    title                       = models.CharField(verbose_name = "게시글 제목", max_length = 100)
    content                     = RichTextUploadingField(verbose_name = "게시글 내용", blank = True)
    image                       = models.ImageField(verbose_name = '이미지 파일', null = True, upload_to = "images/", blank = True)
    publish                     = models.CharField(max_length=1, default='Y')

    DAILY                       = 0
    COOKING                     = 1
    TRAVEL                      = 2
    MOVIE                       = 3
    IT                          = 4

    TOPIC_CHOICES               = [
                                    (DAILY, "일상"),
                                    (COOKING, "요리"),
                                    (TRAVEL, "여행"),
                                    (MOVIE, "영화"),
                                    (IT, "IT")
                                  ]


    topic                       = models.IntegerField(choices=TOPIC_CHOICES, default=DAILY, verbose_name='토픽이름')
    posted_date                 = models.DateTimeField(verbose_name = "게시일", auto_now_add=True)
    updated_date                = models.DateTimeField(verbose_name = "수정일", auto_now_add=True)
    views                       = models.PositiveIntegerField(default = 0)

    # 외래키
    # CASCADE : 외래키가 바라보는 값이 삭제될때 외래키를 포함하는 모델 인스턴스(row)도 삭제된다.
    user                        = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = "유저", default='')



    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name            = '아티클'
        verbose_name_plural     = '아티클 목록'

class Tag(models.Model):
    tag_name = models.CharField(max_length=50, verbose_name='태그 이름')
    # 다른 필드 추가 가능

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = '태그'
        verbose_name_plural = '태그 목록'