from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass 


class Post(models.Model):
    text = models.TextField(blank=False)
    date_time = models.DateTimeField(auto_now_add=True)    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"Post {self.id} | Created by {self.author}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user.username} follows {self.user_followed.username}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_liked")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_liked")

    def __str__(self):
        return f"{self.user.username} liked {self.post}"