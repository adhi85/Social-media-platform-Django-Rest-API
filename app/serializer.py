from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import serializers

from .models import Follow,Post,Like,Comment


User = get_user_model()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ['id', 'follower', 'followee']
        read_only = True

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'post','comment']

class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField('get_comments')

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created', 'user', 'likes','comments']
        read_only_fields = ['id', 'user', 'created']

    def get_likes(self, post):
        likes = post.likes.all()
        return LikeSerializer(likes, many=True).data
    def get_comments(self, post):
        comments = Comment.objects.filter(post = post )
        return CommentSerializer(comments, many = True).data
