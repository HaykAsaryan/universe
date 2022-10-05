import random
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=30) 
    email = models.EmailField()
    verification_code = models.CharField(max_length=254)
    image = models.ImageField(default='/profile_pics/default/default.jpg', upload_to='profile_pics')

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    title = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)
    likes_count = models.PositiveIntegerField(default=0)
 
    def __str__(self):
        return f'{self.user.username}\'s Post- {self.title}'

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} liked {self.post}"
 