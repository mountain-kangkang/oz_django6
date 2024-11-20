from logging import raiseExceptions

from django.db.models import F

from tabom.models import Article, Like, User


def do_like(user_id: int, article_id: int) -> Like:
    # objects 메니저 객체
    # like_exists = Like.objects.filter(user_id=user_id, article_id=article_id).exists()
    # article = Article.objects.get(id=article_id)
    like = Like.objects.create(user_id=user_id, article_id=article_id)
    # article.like_count += 1  # 주의 : 만약 like_count가 None이 될 수 있다면 None체크를 먼저해야한다
    # article.save()
    Article.objects.filter(id=article_id).update(like_count=F("like_count") + 1)

    return like


def undo_like(user_id: int, article_id: int) -> None:
    # 삭제할 데이터가 없어도 아무일도 일어나지 않는다

    """
    요구사항
    삭제 성공 -> 삭제된 좋아요 개수만큼 like_count 차감
    삭제 실패 -> like_count를 차감하지 않는다
    삭제를 성공했는지, 실패했는지, 성공을 했다면 몇 개를 삭제했는지 알 수 있는 방법?
    제일 좋은 방법 : django 문서 정독 - 문서가 많고 영어고 어렵다
    다음 좋은 방법 : 디버깅
        중단점을 먼저 찍는다.
        코드를 실행할 방법도 모른다면 : 전체 테스트 슈트를 디버그 모드로 실행한다.
    """

    deleted_cnt, _ = Like.objects.filter(user_id=user_id, article_id=article_id).delete()
    if deleted_cnt:  # python 에는 Falsy와 Truthy의 개념이 있다
        article = Article.objects.get(id=article_id)
        article.like_count -= 1
        article.save()
