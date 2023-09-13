from django.db import models

class Topic(models.Model):

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


    topic_id                    = models.AutoField(primary_key = True, verbose_name = "토픽ID" )
    topic_name                  = models.IntegerField(choices=TOPIC_CHOICES, default=DAILY, verbose_name='토픽이름')

    
    def __str__(self):
        return f"{self.topic_name}"

    class Meta:
        verbose_name            = '토픽'
        verbose_name_plural     = '토픽 목록'


class Article(models.Model):
    article_id                  = models.AutoField(primary_key = True, verbose_name = "게시글ID")
    title                       = models.CharField(verbose_name = "게시글 제목", max_length = 100)
    content                     = models.TextField(verbose_name = "게시글 내용")
    image                       = models.ImageField(verbose_name = '이미지 파일', null = True, upload_to = "images/", blank = True)
    posted_date                 = models.DateTimeField(verbose_name = "게시일", auto_now_add=True)
    updated_date                = models.DateTimeField(verbose_name = "수정일", auto_now_add=True)
    deleted_date                = models.DateTimeField(verbose_name = "삭제일")
    views                       = models.PositiveIntegerField(default = 0)

    # 외래키
    # CASCADE : 외래키가 바라보는 값이 삭제될때 외래키를 포함하는 모델 인스턴스(row)도 삭제된다.
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE, verbose_name = "토픽ID")

    
    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name            = '아티클'
        verbose_name_plural     = '아티클 목록'

