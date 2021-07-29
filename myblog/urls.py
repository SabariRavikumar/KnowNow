from django.urls import path, include
from .views import HomeView, BlogDetialView, Search, Joinus, CatList, FavPostView, FavCatView, Privacy ,UserNotification, Aboutus ,Contact, CategoryView, AddPostView, AddCategory, UpdatePostView, DeletePostView, LikeView



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', Aboutus, name='about'),
    path('privacy_policy/', Privacy, name='privacy'),
    path('notification/', UserNotification, name='notification'),
    path('addpost/', AddPostView.as_view(), name='addpost'),
    path('blog/read=da212ijna<int:pk>1edsdjh', BlogDetialView.as_view(), name='blog'),
    path('category/<str:cats>', CategoryView, name='cat'),
    path('addcat',AddCategory.as_view(), name='addcat'),
    path('search/', Search, name='search'),
    path('contact/', Contact, name='contact'),
    path('joinus/', Joinus, name='joinus'),
    path('blog/edit/<int:pk>', UpdatePostView.as_view(), name='update_post'),
    path('blog/delete/<int:pk>', DeletePostView.as_view(), name='delete_post'),
    path('like/<int:pk>',LikeView,name='like_post'),
    path('favcat/<str:cats>',FavCatView, name='fav_cat'),
    path('favpost/<int:pk>',FavPostView, name='fav_post'),
    path('category/',CatList, name='cat_list'),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),

]
