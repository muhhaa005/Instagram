from django_filters import FilterSet
from .models import Post, Follow

class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'user' : ['exact'],
            'description': ['exact'],
        }
