from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [

        path('',views.Routes, name = 'routes'),
        path("api/authenticate/", TokenObtainPairView.as_view()),
        path("api/token/refresh/", TokenRefreshView.as_view()),

        path('api/follow/<int:user_id>/', views.FollowUserView.as_view(), name="follow-a-user"),
        path('api/unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name="unfollow-a-user"),
        path('api/user/', views.GetUserView.as_view(), name="get_user"),  

        path('api/post/', views.CreatePostView.as_view(), name="create-post"),   
        path('api/post/<int:pk>/', views.GetUpdateDeletePostView.as_view(), name='get-update-delete-post'),
        path('api/like/<int:pk>/', views.LikePostView.as_view(), name='like-post'),
        path('api/unlike/<int:pk>/', views.UnlikePostView.as_view(), name='unlike-post'),

        path('api/comment/<int:pk>/', views.CommentPostView.as_view(), name='like-post'),
        path('api/all_posts/', views.ListAllPostsView.as_view(), name='list-all-post'),
]