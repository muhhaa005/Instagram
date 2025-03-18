from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework.exceptions import ValidationError


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                                       MaxValueValidator(85)], null=True, blank=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    def get_count_follower(self):
        title =self.user_follower.all()
        if title.exists():
            return title.count()
        return 0

    def get_count_following(self):
        title =self.user_following.all()
        if title.exists():
            return title.count()
        return 0

    def get_avg_post(self):
        total = self.user_post.all()
        if total.exists():
            return total.count()
        return 0



class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='user_follower')
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True, related_name='user_following')
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower}'

    class Meta:
        unique_together = ('follower', 'following')



class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='user_post')
    image = models.ImageField(upload_to='post_images', null=True, blank=True)
    video = models.FileField(upload_to='post_videos', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def clean(self):
        super().clean()
        if not self.image and not self.video:
            raise ValidationError('Choose minimum one of (image, video)!')

    def get_count_post_like(self):
        total = self.post_like.all()
        if total.exists():
            return total.count()
        return 0

    def get_count_comment(self):
        total = self.comment_post.all()
        if total.exists():
            return total.count()
        return 0


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')
    like = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.like}'

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    text = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_count_comment_like(self):
        total = self.comment_like.all()
        if total.exists():
            return total.count()
        return 0


    def __str__(self):
        return f'{self.user}, {self.text}'


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_like')
    like = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.like}, {self.comment}'

    class Meta:
        unique_together = ('user', 'comment')


class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='story_post')
    image = models.ImageField(upload_to='story_images', null=True, blank=True)
    video = models.FileField(upload_to='story_videos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    def clean(self):
        super().clean()
        if not self.image and not self.video:
            raise ValidationError('Choose minimum one of (image, video)!')


class Save(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='save_user')


class SaveItem(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    save = models.ForeignKey(Save, on_delete=models.CASCADE, related_name='save_item')
    created_date = models.DateTimeField(auto_now_add=True)

class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateField(auto_now_add=True)

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='chat_images', null=True, blank=True)
    video = models.FileField(upload_to='chat_videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
