from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.

class User(AbstractUser):
    """
    A custom User model
    The `email` field is set as unique and required.
    """

    first_name = None
    last_name = None
    name = models.CharField(_("name"), max_length=300, blank=True)
    email = models.EmailField(_("email"), unique=True)


class Follow(models.Model):
    follower = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='follower', null=True, blank=True)
    followee = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='followee',  null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.follower} follows {self.followee}'


class Post(models.Model):
    title = models.CharField(max_length=30,null=False, blank=False)
    description = models.CharField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} POSTED BY {self.user} '

    class Meta:
        ordering = ('-created',)


class Like(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='liked_posts', null=True, blank=True)
    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name='likes', null=True, blank=True)
    


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE,
                             related_name='commented_posts', null=True, blank=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE,
                             related_name='comments', null=True, blank=True)
    comment = models.CharField(max_length=512, null=False, blank=False)
