from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    posts = models.IntegerField(default=1)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=30) 
    email = models.EmailField()
    verification_code = models.CharField(max_length=254)
    image = models.ImageField(default='/profile_pics/default/default.jpg', upload_to='profile_pics/default')

    def __str__(self):
        return self.user.username

def _upload_path(instance,filename):
    return instance.get_upload_path(filename)

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    username = models.CharField(max_length=30)
    image = models.ImageField(upload_to=_upload_path)
    text = models.TextField()
    date_posted = models.DateTimeField(default = datetime.now())
    likes_count = models.PositiveIntegerField(default=0)
 
    def get_upload_path(self,filename):
        return f"posts/" + str(self.username)+ "/" + str(self.profile.posts) + "/" + filename

    def __str__(self):
        return f'{self.profile.username}\'s Post'
 