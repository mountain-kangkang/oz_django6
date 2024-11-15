from logging import raiseExceptions

from tabom.models import Article, Like, User


def do_like(user_id: int, article_id: int) -> Like:
    # objects 메니저 객체
    # like_exists = Like.objects.filter(user_id=user_id, article_id=article_id).exists()

    return Like.objects.create(user_id=user_id, article_id=article_id)
