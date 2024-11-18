from logging import raiseExceptions

from tabom.models import Article, Like, User


def do_like(user_id: int, article_id: int) -> Like:
    # objects 메니저 객체
    # like_exists = Like.objects.filter(user_id=user_id, article_id=article_id).exists()

    return Like.objects.create(user_id=user_id, article_id=article_id)


def undo_like(user_id: int, article_id: int) -> None:
    # 삭제할 데이터가 없어도 아무일도 일어나지 않는다
    Like.objects.filter(user_id=user_id, article_id=article_id).delete()
