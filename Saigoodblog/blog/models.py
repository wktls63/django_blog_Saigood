from django.db import models

# Create your models here.
class article(models.Model):
    article_id = models.AutoField(primary_key=True)
    temp_saved_at = models.DateTimeField()
    posted_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    deleted_at = models.DateTimeField()
    views = models.PositiveIntegerField(default=0)

    # 외래키
    # CASCADE : 외래키가 바라보는 값이 삭제될때 외래키를 포함하는 모델 인스턴스(row)도 삭제된다.
    username = models.ForeignKey("user", on_delete=models.CASCADE)
    article_detail_id = models.ForeignKey("article_detail", on_delete=models.CASCADE)
    topic_id = models.ForeignKey("topic", on_delete=models.CASCADE)

# TODO : article_detail과 topic 클래스를 추가로 정의해야 합니다.