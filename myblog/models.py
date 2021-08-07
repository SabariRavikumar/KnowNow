from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from taggit.managers import TaggableManager


class Category(models.Model):
    cat_name = models.CharField(max_length=255,unique=True)
    cat_img = models.ImageField(default='default_thumb.jpg',upload_to='category',blank=True)
    cat_view = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    
    def __str__(self):
        return self.cat_name
    
    def get_absolute_url(self):
        return reverse('home')

class Post(models.Model):
    thumbnail = models.ImageField(default='default_thumb.jpg',upload_to='thumbnail',blank=True)
    title = models.CharField(max_length=255)
    post_tag = TaggableManager()
    cat = models.CharField(Category,max_length=100, default="None")
    content = RichTextUploadingField(blank=True, null=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',related_query_name='hit_count_generic_relation')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    likes = models.ManyToManyField(User,related_name='blog_like')

    def total_likes(self):
        return self.likes.count()

    
    def __str__(self):
        return self.title + ' | ' + str(self.author)
    
    def get_absolute_url(self):
        return reverse('blog', args=[self.id,])



class Comment(models.Model):
    post = models.ForeignKey(Post, related_name = "comments", on_delete=models.CASCADE)
    name = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return  '%s - %s - %s' % (self.post.title, self.name, self.body)
    


    