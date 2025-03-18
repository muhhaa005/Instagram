from django.urls import path, include
from rest_framework import routers
from .views import (UserProfileListAPIView, UserProfileEditAPIView, FollowViewSet,
                    PostCreateAPIView, PostListAPIView, PostDetailAPIView, PostLikeCreateAPIView, PostLikeListAPIView, PostLikeDetailAPIView,
                    CommentCreateAPIView, CommentListAPIView, CommentDetailAPIView, CommentLikeCreateAPIView, CommentLikeListAPIView, CommentLikeDetailAPIView,
                    StoryCreateAPIView, StoryListAPIView, StoryDetailAPIView, SaveListAPIView, SaveItemDetailAPIView, RegisterView, LoginView, LogoutView
                    )


router = routers.SimpleRouter()
router.register(r'follows', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),

    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileEditAPIView.as_view(), name='user_edit'),

    path('post_create/', PostCreateAPIView.as_view(), name='post_create'),
    path('post/', PostListAPIView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),

    path('post_like/', PostLikeListAPIView.as_view(), name='post_like_list'),
    path('post_like/<int:pk>/', PostLikeDetailAPIView.as_view(), name='post_like_detail'),
    path('post_like/create/', PostLikeCreateAPIView.as_view(), name='post_like_create'),

    path('comment/', CommentListAPIView.as_view(), name='comment_list'),
    path('comment/<int:pk>/', CommentDetailAPIView.as_view(), name='comment_detail'),
    path('comment/create/', CommentCreateAPIView.as_view(), name='comment_create'),

    path('comment_like/', CommentLikeListAPIView.as_view(), name='comment_like_list'),
    path('comment_like/<int:pk>/', CommentLikeDetailAPIView.as_view(), name='comment_like_detail'),
    path('comment_like/create/', CommentLikeCreateAPIView.as_view(), name='comment_like_create'),

    path('story/', StoryListAPIView.as_view(), name='story_list'),
    path('story/<int:pk>/', StoryDetailAPIView.as_view(), name='story_detail'),
    path('story/create/', StoryCreateAPIView.as_view(), name='story_create'),

    path('save/', SaveListAPIView.as_view(), name='save_list'),
    path('save/<int:pk>/', SaveItemDetailAPIView.as_view(), name='save_detail'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')

]