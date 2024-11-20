from logging import raiseExceptions

from django.db import IntegrityError
from django.test import TestCase

from tabom.models import Article, Like, User
from tabom.services.like_service import do_like, undo_like


class TestLikeService(TestCase):
    def test_a_user_like_an_article(self) -> None:
        # given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # when
        like = do_like(user.id, article.id)

        # then
        # id 가 들어있다는 것은 데이터베이스로부터 id 를 발급받았다는 뜻
        # 즉, 성공적으로 insert가 되었다는 증거임
        self.assertIsNotNone(like.id)
        self.assertEqual(user.id, like.user.id)
        self.assertEqual(article.id, like.article.id)

    def test_a_user_can_like_an_article_only_once(self) -> None:
        # given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # Expect
        like1 = do_like(user.id, article.id)
        # Exception 이 발생하면 통과, 아무일도 안 일어나면 AssertionError 를 일으킨다
        with self.assertRaises(IntegrityError):
            like2 = do_like(user.id, article.id)

    def test_it_should_raise_exception_when_like_an_user_does_not_exist(self) -> None:
        # Given
        invalid_user_id = 9988
        article = Article.objects.create(title="test_title")

        # Expect
        with self.assertRaises(IntegrityError):
            do_like(invalid_user_id, article.id)

    # def test_it_should_raise_exception_when_like_an_article_does_not_exist(self) -> None:
    #     # Given
    #     user = User.objects.create(name="test")
    #     invalid_article_id = 9988
    #
    #     # Expect
    #     with self.assertRaises(IntegrityError):
    #         do_like(user.id, invalid_article_id)

    def test_like_count_should_increase(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # When
        do_like(user.id, article.id)

        # Then
        result_article = Article.objects.get(id=article.id)
        self.assertEqual(1, result_article.like_count)

    def test_a_user_can_undo_like(self) -> None:
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")
        like = Like.objects.create(user=user, article=article)

        undo_like(user.id, article.id)

        with self.assertRaises(Like.DoesNotExist):
            Like.objects.get(id=like.id)

        # Then 절에서 DoesNotExist 로 검사하는거 말고 다른 방법이 있지 않을까?


"""
http POST http://127.0.0.1:8000/api/v1/likes/ user_id:=1 article_id:=15 &
"""
