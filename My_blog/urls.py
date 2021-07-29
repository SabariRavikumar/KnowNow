"""My_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from users.views import register, logIn, logOut, DeleteUserView, ProfileView, EditProfile, FollowView, PasswordsChangeView
# from myblog.sitemaps import StaticViewsSitemap,PostSitemap,ProfileSitemap
# from django.contrib.sitemaps.views import sitemap

# sitemaps = {
#     'sitemap':StaticViewsSitemap,
#     'posts':PostSitemap,
#     'profile':ProfileSitemap,
# }

urlpatterns = [
    # path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
    #  name='django.contrib.sitemaps.views.sitemap'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', logIn, name='login'),
    path('logout/', logOut, name='logout'),
    path('profile/aaa235423<int:pk>5kfjsdlaaa/',ProfileView.as_view(),name='profile'),
    path('profile/delete/aaa235423<int:pk>5kfjsdlaaa/',DeleteUserView.as_view(), name='delete_user' ),
    path('edit_profile', EditProfile, name='edit_profile'),
    path('follow/<int:pk>', FollowView, name='follow_user'),
    path('password/',PasswordsChangeView.as_view(), name='password'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'), name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_done.html'), name='password_reset_complete'),
    path('',include('myblog.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
