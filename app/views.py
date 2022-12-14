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
from rest_framework.decorators import permission_classes,api_view
from rest_framework.permissions import AllowAny

from . helping import IsOwnerOrReadOnly, CreateOrDestroyView

from django.http import JsonResponse
# Create your views here.

@api_view(['GET'])
@permission_classes((AllowAny, ))
def Routes(request):
    routes = [
        'GET /api/',
        'All OPERATIONS',
        'POST /api/authenticate/ : Generate the JWT token for the user ',
        'POST /api/follow/{id} authenticated user would follow user with {id}',
        'POST /api/unfollow/{id} authenticated user will unfollow a user with {id}',
        'GET /api/user authenticate the request and return the respective user profile.',
        'POST api/posts/ add a new post created by the authenticated user.',
        '  -> Input: Title, Description ' 
        '=>RETURN: Post-ID, Title, Description, Created Time(UTC).',
        'DELETE api/posts/{id}  delete post with {id} created by the authenticated user.',
        'POST /api/like/{id}  like the post with {id} by the authenticated user.',
        'POST /api/unlike/{id}  unlike the post with {id} by the authenticated user.',
        'POST /api/comment/{id} add comment for post with {id} by the authenticated user.',
            '- Input: Comment'
            '- Return: Comment-ID',
        "GET api/posts/{id}  return a single post with {id} populated with its number of likes and comments",
        "GET /api/all_posts  return all posts created by authenticated user sorted by post time",
        

    ]
    return Response(routes)

def home(request):
    return HttpResponse("<h1>Home </h1> <hr>")
User = get_user_model()

class FollowUserView(CreateAPIView, mixins.DestroyModelMixin):
    """
    post: follow user with <user_id>
    
    """
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
    get: authenticate the request and return the respective user profile.
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
    """
    post: unlike post
    """
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
    get: list all posts of authenticated user
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        print(self.request.GET)  
        posts = self.queryset.filter(user__id=self.request.user.id)
        return posts.order_by('-created')