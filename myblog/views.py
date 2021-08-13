from django.shortcuts import render, get_object_or_404, redirect, reverse   
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from community.models import JoinUs
from .forms import PostForm, CategoryForm, CommentForm, PostUpdateForm, JoinUsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from hitcount.views import HitCountDetailView
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.core.mail import send_mail
from django.conf import settings
from Notifications.models import Notification
from users.models import Profile
from django.contrib.auth.models import User
from django.core.paginator import Paginator


class HomeView(ListView):
    model = Post
    paginate_by = 6
    template_name = 'blog/home.html'
    ordering = ['-date_posted']

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            id = request.POST.get('id')
            user = request.POST.get('user')
            if id:
                note = get_object_or_404(Notification, id=id)
                note.is_seen = True
                note.save()
            if user:
                notes = Notification.objects.filter(user=user)
                for note in notes:
                    note.is_seen = True
                    note.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    def get_context_data(self, *args, **kwargs):
        notification = Notification.objects.filter(user=self.request.user.id, is_seen=False).order_by('-date')  
        cat_tab = Category.objects.all().order_by('cat_view')[:9]
        pop_posts = Post.objects.all().order_by('hit_count_generic')[:5]
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context['cat_tab'] = cat_tab
        context['pop_posts'] = pop_posts
        context['notification'] = notification
        context['active1'] = 'nav-active'
        return context 

def Aboutus(request):
    if request.user.is_authenticated:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by('-date') 
    else:
        notification = None  
    post = Post.objects.all().count()
    user = User.objects.all()
    cat_tab = Category.objects.all()[:10]
    community = JoinUs.objects.all()
    if post == 0:
        pst = 0 
    else:
        pst = post.count()
 
    context = {
        'post':pst,
        'usr':user,
        'com':community,
        'notification':notification,
        'cat_tab':cat_tab,
    }
    return render(request,'blog/aboutus.html', context)

def Privacy(request):
    if request.user.is_authenticated:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by('-date') 
    else:
        notification = None
    cat_tab = Category.objects.all()[:10]
    context = {
            'cat_tab':cat_tab,
            'notification':notification,
    }
    return render(request,'blog/privacypolicy.html',context)

class BlogDetialView(HitCountDetailView,DetailView):
    model = Post
    template_name = 'blog/blogview.html'
    form = CommentForm
    count_hit = True

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post = self.get_object()
        if form.is_valid():
            form.instance.post = post
            form.instance.name = request.user
            form.save()
            if request.user != post.author:
                note = Notification(notification_type=2, post=post, sender=request.user, user=post.author)
                note.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

    def get_context_data(self, *args, **kwargs):
        cat_tab = Category.objects.all()[:10]
        similar_post = self.object.post_tag.similar_objects()[:5]
        context = super(BlogDetialView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        post_filter = Post.objects.filter(author=stuff.author).order_by('hit_count_generic')[:10]
        total_likes = stuff.total_likes()
        liked_user = stuff.likes.all()
        liked = False
        followed = False
        added = False
        if self.request.user.is_authenticated:
            pro_stuff = get_object_or_404(Profile, id=self.request.user.id)
            if stuff.likes.filter(id=self.request.user.id).exists():
                liked = True
            if pro_stuff.following.filter(id=stuff.author.id):
                followed = True
            if pro_stuff.fav_post.filter(id=stuff.id):
                added=True
            notification = Notification.objects.filter(user=self.request.user, is_seen=False).order_by('-date')  
            context['notification'] = notification
        context["total_likes"] = total_likes
        context["similar_post"] = similar_post
        context['liked_user'] = liked_user
        context['added'] = added
        context['liked'] = liked
        context['followed'] = followed
        context['form'] = self.form
        context["post_filter"] = post_filter
        context["cat_tab"] = cat_tab
        context["title"] = stuff.title
        return context 

def CategoryView(request, cats):
    cat = get_object_or_404(Category, cat_name=cats)
    fav_cat_user = Profile.objects.filter(fav_cat=cat.id)
    added = False
    if request.user.is_authenticated:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by('-date') 
        stuff = get_object_or_404(Profile, id=request.user.id)
        if stuff.fav_cat.filter(id = cat.id):
            added = True
    else:
        notification=None
    cat_tab = Category.objects.all()[:10]
    category_post = Post.objects.filter(cat=cats).order_by('-date_posted')
    # paginator = Paginator(category_post, 8) 
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    context = {
        'title':cats,
        'notification':notification,
        # 'page_obj': page_obj, 
        'added':added,
        'cat_tab':cat_tab,
        'cat_post':category_post,
        'fav_cat_user':fav_cat_user,
    }
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(cat)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    return render(request, 'blog/category.html', context)

def CatList(request):
    cat = Category.objects.all()
    cat_tab = Category.objects.all()[:10]
    if request.user.is_authenticated:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by('-date') 
    else:
        notification=None
    context = {
        'cat':cat, 
        'notification':notification, 
        'title':"Category",
        'cat_tab':cat_tab
        }
    return render(request, 'blog/categoryList.html', context)

class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            cat = Category.objects.get(cat_name=request.POST.get('cat')) 
            post = form.save()
            fav_cat_user = Profile.objects.filter(fav_cat=cat)
            for user in fav_cat_user:
                if user.user is not request.user:
                    note = Notification(notification_type=6, post=post, sender=request.user, user=user.user)
                    note.save()
            field_name = 'followers'
            obj = Profile.objects.get(id=request.user.profile.id)
            field_object = Profile._meta.get_field(field_name)
            follower = field_object.value_from_object(obj)
            for user in follower:
                note = Notification(notification_type=4, post=post, sender=request.user, user=user)
                note.save()
        return redirect(reverse('blog', args=[str(post.pk)]))
        
    def get_context_data(self, *args, **kwargs):
        cat = Category.objects.all()
        cat_tab = Category.objects.all()[:10]
        notification = Notification.objects.filter(user=self.request.user, is_seen=False).order_by('-date') 
        context = super(AddPostView, self).get_context_data(*args, **kwargs)
        context["title"] = 'New Post'
        context['cat_tab'] = cat_tab
        context['cat'] = cat
        context['notification'] = notification
        context['active2'] = 'nav-active'
        return context


class AddCategory(LoginRequiredMixin, CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'
    login_url = 'login'
    
    def get_context_data(self, *args, **kwargs):
        cat_tab = Category.objects.all()[:10]
        notification = Notification.objects.filter(user=self.request.user, is_seen=False).order_by('-date') 
        context = super(AddCategory, self).get_context_data(*args, **kwargs)
        context["title"] = 'Add Category'
        context['notification'] = notification
        context['cat_tab'] = cat_tab
        return context

    def get_success_url(self):
        return reverse('addpost')

def Search(request):
    if request.user.is_authenticated:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by('-date') 
    else:
        notification = None    
    cat_tab = Category.objects.all()[:10]
    query = request.POST['search']
    if Post.objects.filter(title__icontains=query):
        posts = Post.objects.filter(title__icontains=query).order_by('date_posted')
        user = None
    elif Post.objects.filter(cat__icontains=query):
        posts = Post.objects.filter(cat__icontains=query).order_by('date_posted')
        user = None
    elif Post.objects.filter(author__username=query) or User.objects.filter(username__icontains=query):
        posts = Post.objects.filter(author__username=query).order_by('date_posted')
        user = User.objects.filter(username__icontains=query)
    else:
        posts = None
        user = None
    context = {
        'posts':posts,
        'usr':user, 
        'title':f"search Result - {query}",
        'notification':notification,
        'cat_tab':cat_tab
        }
    return render(request, 'blog/search.html', context)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    form_class = PostUpdateForm
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.POST.get('id'))
        if request.method == 'POST':
            form = PostUpdateForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                field_name = 'followers'
                obj = Profile.objects.get(id=request.user.profile.id)
                field_object = Profile._meta.get_field(field_name)
                follower = field_object.value_from_object(obj)
                for user in follower:
                    note = Notification(notification_type=5, post=post, sender=request.user, user=user)
                    note.save()
            return redirect(reverse('blog', args=[str(post.pk)]))
        else:
            form = PostUpdateForm(insatnce=post)

    def get_success_url(self):
        return reverse('blog', args=[str(self.object.pk)])

    def get_context_data(self, *args, **kwargs):
        cat_tab = Category.objects.all()[:10]
        notification = Notification.objects.filter(user=self.request.user, is_seen=False).order_by('-date') 
        context = super(UpdatePostView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Update Post'
        context['notification'] = notification
        context['cat_tab'] = cat_tab
        return context

class DeletePostView(LoginRequiredMixin,DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    login_url = 'login'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        cat_tab = Category.objects.all()[:10]
        notification = Notification.objects.filter(user=self.request.user, is_seen=False).order_by('-date') 
        context = super(DeletePostView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Delete Post'
        context['notification'] = notification
        context['cat_tab'] = cat_tab
        return context

@login_required
def LikeView(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True 
        if request.user !=  post.author:
            note = Notification(notification_type=1, sender=request.user, user=post.author, post=post)
            note.save()
    return HttpResponseRedirect(reverse('blog', args=[str(pk)]))


@login_required
def FavCatView(request,cats):
    cat = get_object_or_404(Category, cat_name=cats)
    usr = get_object_or_404(Profile, id=request.user.id)
    added = False
    if usr.fav_cat.filter(id=cat.id).exists():
        usr.fav_cat.remove(cat)
        liked = False
    else:
        usr.fav_cat.add(cat)
        added = True
    return HttpResponseRedirect(reverse('cat', args=[str(cats)]))

@login_required
def FavPostView(request,pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    usr = get_object_or_404(Profile, id=request.user.id)
    added = False
    if usr.fav_post.filter(id=post.id).exists():
        usr.fav_post.remove(post)
        added = False
    else:
        usr.fav_post.add(post)
        added = True 
    return HttpResponseRedirect(reverse('blog', args=[str(pk)]))



def Contact(request):
    if request.user.is_authenticated:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by('-date') 
    else:
        notification = None
    cat_tab = Category.objects.all()[:10]
    if request.method == 'POST':
        name = request.POST['name']
        mail = request.POST['mail']
        msg = request.POST['message']

        send_mail(
            f"Message From {name}...Email {mail}",
            f"Message: {msg}\n mail :{mail}",
            mail,
            ['sabariravissl20@gmail.com'], 
        )

        return render(request, 'blog/contact.html', {'name':name,'cat_tab':cat_tab, 'notification':notification})
    else:
        return render(request, 'blog/contact.html',{'cat_tab':cat_tab,'notification':notification})

def Joinus(request):
    if request.user.is_authenticated:
        notification = Notification.objects.filter(user=request.user, is_seen=False).order_by('-date') 
    else:
        notification = None
    
    cat_tab = Category.objects.all()[:10]
    if request.method == 'POST':
        form = JoinUsForm(request.POST)
        if form.is_valid():
            form.save()
            name = request.POST['name']
            mail = request.POST['email']
            send_mail(
                f"Welcome {name}",
                f"Thanks For Joining us",
                'sabariravissl20@gmail.com',
                [mail]
            )
            return render(request, 'blog/joinus.html', {'name':name,'cat_tab':cat_tab, 'notification':notification})
    else:
        form = JoinUsForm()
    return render(request, 'blog/joinus.html',{'form':form,'cat_tab':cat_tab,'notification':notification})

def UserNotification(request):
    cat_tab = Category.objects.all()[:10]
    notification = Notification.objects.filter(user=request.user, is_seen=False).order_by('-date')
    noti = Notification.objects.filter(user=request.user).order_by('-date')
    context = {
        'cat_tab':cat_tab,
        'noti':noti,
        'notification':notification
    }
    return render(request, 'blog/notification.html', context)