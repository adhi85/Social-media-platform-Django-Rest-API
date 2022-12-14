from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from .serializer import FollowSerializer , PostSerializer , LikeSerializer, CommentSerializer
from .models import Follow, Post , Like, Comment
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404, CreateAPIView, ListAPIView
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly, CreateOrDestroyView

from django.http import JsonResponse
# Create your views here.

def home(request):
    return HttpResponse("<h1>Home </h1> <hr>")
User = get_user_model()

class FollowUserView(CreateAPIView, mixins.DestroyModelMixin):
    """
    post: follow user with <user_id>
    
    """
    # lookup_field = 'user_id'  # not needed here but can be useful to replace 'pk' with something else
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()

    def perform_create(self, serializer):
        user_to_follow = get_object_or_404(User, id=self.kwargs.get('user_id'))

        if (user_to_follow == self.request.user) :
            raise PermissionDenied('Can not follow yourself')

        already_following = Follow.objects.filter(follower=self.request.user, followee=user_to_follow).exists()

        if already_following:
            raise PermissionDenied('already following')

        
        serializer.save(follower=self.request.user, followee=user_to_follow)
        

class UnfollowUserView(CreateAPIView,mixins.DestroyModelMixin):
    # delete: unfollow user with user_id

    def post(self, request, *args, **kwargs):
        user_to_unfollow = get_object_or_404(User, id=self.kwargs.get('user_id'))
        follow = get_object_or_404(Follow, follower=self.request.user, followee=user_to_unfollow)
        follow.delete()
        return Response(status=204)


class GetUserView(APIView):
    """
    get: get all users the logged in user follows
    """
    def get(self,request):
        following = Follow.objects.filter(follower=request.user)
        following = len(following)
        followers = Follow.objects.filter(followee=request.user)
        followers = len(followers)
        responseData = {
            'username' : request.user.username,
            'following': following,
            'followers' : followers
        }
        return JsonResponse(responseData)

        
        
class CreatePostView(CreateAPIView):
    """
    post: create a post (logged in, cannot create posts for other users)
    """
    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        new_post = serializer.save(user=self.request.user)

class GetUpdateDeletePostView(RetrieveUpdateDestroyAPIView):
    """
    get: get a single specific post. (Logged in users only)
    put: edit a post (owning user only).
    delete: delete a post (owning user only).
    """

    permission_classes = (IsOwnerOrReadOnly,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

class LikePostView(CreateOrDestroyView):
    """
    post: like post
    """
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        already_liked = Like.objects.filter(user=self.request.user, post=post).exists()

        if already_liked:
            raise PermissionDenied('already liked') 
            
        serializer.save(user=self.request.user, post=post)  # prevents "impersonating" other users



class UnlikePostView(CreateOrDestroyView):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        like = get_object_or_404(Like, user=self.request.user, post=post)
        like.delete()
        return Response(status=204)

class CommentPostView(CreateOrDestroyView):
    """
    post: comment post
    """
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('pk'))
    
            
        serializer.save(user=self.request.user, post=post)  # prevents "impersonating" other users


class ListAllPostsView(ListAPIView):
    """
    get: list all posts of a user
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        print(self.request.GET)  # this would print all querystring params
        posts = self.queryset.filter(user__id=self.request.user.id)
        return posts.order_by('-created')