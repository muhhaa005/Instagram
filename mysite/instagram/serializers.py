from rest_framework import serializers
from .models import UserProfile, Follow, Post, PostLike, Comment, CommentLike, Story, Save, SaveItem
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'age', 'phone_number', 'bio', 'image', 'website')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Post
        fields = ['id', 'user', 'image']



class UserProfileSerializer(serializers.ModelSerializer):
    count_follower = serializers.SerializerMethodField()
    count_following = serializers.SerializerMethodField()
    avg_post = serializers.SerializerMethodField()
    user_post = PostListSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'first_name', 'last_name', 'image', 'bio','age', 'website', 'count_follower', 'count_following', 'avg_post', 'user_post']

    def get_count_follower(self, obj):
        return obj.get_count_follower()

    def get_count_following(self, obj):
        return obj.get_count_following()

    def get_avg_post(self, obj):
        return obj.get_avg_post()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class PostLikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ['like']

class PostLikeDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))
    user = UserProfileSimpleSerializer()

    class Meta:
        model = PostLike
        fields = ['user', 'like', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post']


class StoryListSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Story
        fields = ['id', 'user']


class PostDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    post_like = PostLikeListSerializer(many=True, read_only=True)
    count_post_like = serializers.SerializerMethodField()
    comment_post = CommentListSerializer(many=True, read_only=True)
    count_comment = serializers.SerializerMethodField()
    story_post = StoryListSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))


    class Meta:
        model = Post
        fields = ['user', 'image', 'video', 'story_post', 'post_like', 'count_post_like', 'description', 'count_comment', 'comment_post', 'created_at']

    def get_count_post_like(self, obj):
        return obj.get_count_post_like()

    def get_count_comment(self, obj):
        return obj.get_count_comment()


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = '__all__'



class CommentDetailSerializer(serializers.ModelSerializer):
    count_comment_like = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))
    user = UserProfileSimpleSerializer()

    class Meta:
        model = Comment
        fields = ['user', 'text', 'parent', 'count_comment_like', 'created_at']

    def get_count_comment_like(self, obj):
        return obj.get_count_comment_like()


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = '__all__'


class CommentLikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['like']

class CommentLikeDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))
    user = UserProfileSimpleSerializer()

    class Meta:
        model = CommentLike
        fields = ['user', 'like', 'created_at']


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = '__all__'


class StoryDetailSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    created_at = serializers.DateTimeField(format('%d-%m-%Y'))

    class Meta:
        model = Story
        fields = ['user', 'image', 'video', 'created_at']


class SaveItemSerializer(serializers.ModelSerializer):
    post = PostListSerializer(read_only=True)
    post_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True, source='post')

    class Meta:
        model = SaveItem
        fields = ['id', 'post', 'post_id']


class SaveSerializer(serializers.ModelSerializer):
    user = UserProfileSimpleSerializer()
    save_item = SaveItemSerializer(many=True, read_only=True)

    class Meta:
        model = Save
        fields = ['id', 'user', 'save_item']


