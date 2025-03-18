from django.core.serializers import serialize, get_serializer
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import UserProfile, Follow, Post, PostLike, Comment, CommentLike, Story, Save, SaveItem
from .serializers import (UserProfileSerializer, UserProfileCreateSerializer, FollowSerializer,
                          PostSerializer, PostListSerializer, PostDetailSerializer,
                          PostLikeSerializer, PostLikeListSerializer, PostLikeDetailSerializer,
                          CommentSerializer, CommentListSerializer, CommentDetailSerializer,
                          CommentLikeSerializer, CommentLikeListSerializer, CommentLikeDetailSerializer,
                          StorySerializer, StoryListSerializer, StoryDetailSerializer, SaveSerializer,
                          SaveItemSerializer, UserSerializer, LoginSerializer
)
from .filters import PostFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class UserProfileEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileCreateSerializer
    permission_classes = [permissions.IsAuthenticated]



class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['follower', 'following']
    permission_classes = [permissions.IsAuthenticated]


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = PostFilter
    search_fields = ['user']
    permission_classes = [permissions.IsAuthenticated]

class PostLikeCreateAPIView(generics.CreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostLikeListAPIView(generics.ListAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeListSerializer
    permission_classes = [permissions.IsAuthenticated]

class PostLikeDetailAPIView(generics.RetrieveAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentDetailAPIView(generics.RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentLikeCreateAPIView(generics.CreateAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentLikeListAPIView(generics.ListAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeListSerializer
    permission_classes = [permissions.IsAuthenticated]

class CommentLikeDetailAPIView(generics.RetrieveAPIView):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class StoryCreateAPIView(generics.CreateAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticated]

class StoryListAPIView(generics.ListAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryListSerializer
    permission_classes = [permissions.IsAuthenticated]

class StoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Story.objects.all()
    serializer_class = StoryDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class SaveListAPIView(generics.ListAPIView):
    queryset = Save.objects.all()
    serializer_class = SaveSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs ):
        save, created = Save.objects.get_or_create(user=request.user)
        serializer = get_serializer(Save)
        return Response(serializer.data)



class SaveItemDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = SaveItem.objects.all()
    serializer_class = SaveItemSerializer
    permission_classes = [permissions.IsAuthenticated]

