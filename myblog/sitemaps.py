# from django.contrib.sitemaps import Sitemap
# from django.urls import reverse
# from .models import Post
# from users.models import Profile

# class StaticViewsSitemap(Sitemap):
#     priority = 0.5
#     changefreq = "daily"
#     def items(self):
#         return [
#             'home',
#             'about',
#             'contact',
#         ]

#     def location(self,item):
#         return reverse(item)

# class PostSitemap(Sitemap):
#     def items(self):
#         return Post.objects.all()
# class ProfileSitemap(Sitemap):
#     def items(self):
#         return Profile.objects.all()