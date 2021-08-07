from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from myblog.models import Category, Post


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default=None,upload_to='profile_pics',blank=True)
    cover_img = models.ImageField(default=None,upload_to='cover_pics',blank=True)
    about = models.TextField(User)
    fb = models.URLField(max_length=255,null=True, blank=True,default="")
    insta = models.URLField(max_length=255,null=True, blank=True)
    linkedin = models.URLField(max_length=255,null=True, blank=True)
    twitter = models.URLField(max_length=255,null=True, blank=True)
    website = models.URLField(max_length=255,null=True, blank=True)
    followers = models.ManyToManyField(User,related_name='follower')
    following = models.ManyToManyField(User,related_name='following')
    fav_cat = models.ManyToManyField(Category, related_name='fav_cat')
    fav_post = models.ManyToManyField(Post, related_name="fav_post")

    def total_followers(self):
        return self.followers.count()

    def total_following(self):
        return self.following.count()
    

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('profile', args=[self.id,])

