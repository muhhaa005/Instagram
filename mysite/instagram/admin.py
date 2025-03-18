from django.contrib import admin
from .models import (UserProfile, Follow, Post, PostLike, Comment, CommentLike, Story, Save, SaveItem)

admin.site.register(UserProfile)
admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(Story)
admin.site.register(Save)
admin.site.register(SaveItem)
