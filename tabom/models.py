from django.db import models
from django.db.models import UniqueConstraint


class baseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class User(baseModel):
    name = models.CharField(max_length=50)


class Article(baseModel):
    title = models.CharField(max_length=255)
    like_count = models.IntegerField(default=0)


class Like(baseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "article"], name="UIX_user_article"),
        ]
