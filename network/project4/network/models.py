from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} posted on {self.created_date}: {self.content} [{self.likes} likes]"

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')

    def __str__(self):
        return f"{self.follower} followed {self.following}"
    
    class Meta:
        # Add a unique constraint to ensure each combination of follower and following is unique
        unique_together = ('follower', 'following')