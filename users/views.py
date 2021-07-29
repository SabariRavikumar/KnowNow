from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import DetailView, DeleteView
from django.views import generic
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User
from .models import Profile
from myblog.models import Post, Category
from Notifications.models import Notification
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.http import is_safe_url
from django.conf import settings


def register(request):
    cat_tab = Category.objects.all()[:10]
    nxt = request.POST.get('next')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            # username = form.cleaned_data.get('username')
            # email = form.cleaned_data.get('email')
            messages.success(request, f'Account created succesfully')                
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            if nxt:
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            else:
                return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html',{'form':form, 'cat_tab':cat_tab,'title':'Sign Up'})

def logIn(request):
    cat_tab = Category.objects.all()[:10]
    nxt = request.GET.get("next")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {username}!')
            
            if nxt:
                return redirect(nxt)
            else:
                return redirect('home')
        else:
            messages.info(request, 'Incorrect Username or Password')
    return render(request, 'users/login.html', {'title':'Log In', 'cat_tab':cat_tab})

def logOut(request):
    logout(request)
    return redirect('home')

@login_required
def EditProfile(request):
    cat_tab = Category.objects.all()[:10]
    notification = Notification.objects.filter(user=request.user.id, is_seen=False).order_by('-date')
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your profile was updated successfully')
            return redirect('profile', request.user.id)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)


    context ={
        'notification':notification,
        'u_form':u_form,
        'p_form':p_form,
        'title':'Edit Profile',
        'cat_tab':cat_tab,
    }
    return render(request,'users/edit_profile.html',context)

class PasswordsChangeView(SuccessMessageMixin,LoginRequiredMixin,PasswordChangeView):
    form_class = PasswordChangeForm
    template_name='users/change_password.html'
    success_url = reverse_lazy('edit_profile')
    success_message = "Your passowrd was changed successfully"

    def get_context_data(self, *args, **kwargs):
        cat_tab = Category.objects.all()[:10]
        notification = Notification.objects.filter(user=self.request.user.id, is_seen=False).order_by('-date') 
        context = super(PasswordChangeView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Reset Password'
        context["notification"] = notification
        context['cat_tab'] = cat_tab
        return context


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'

    def get_context_data(self, *args, **kwargs):
        cat_tab = Category.objects.all()[:10]
        notification = Notification.objects.filter(user=self.request.user.id, is_seen=False).order_by('-date') 
        context = super(ProfileView, self).get_context_data(*args, **kwargs)
        total_post =  Post.objects.filter(author=self.kwargs['pk']).count()
        post_list = Post.objects.filter(author=self.kwargs['pk'])
        stuff = get_object_or_404(Profile, id=self.kwargs['pk'])
        fav_post = stuff.fav_post.all()
        total_followers = stuff.total_followers()
        total_following = stuff.total_following()
        following = stuff.following.all()
        followers = stuff.followers.all()
        followed = False
        if stuff.followers.filter(id=self.request.user.id).exists():
            followed = True
        context['total_post'] = total_post
        context['total_followers'] = total_followers
        context['followers'] = followers
        context['total_following'] = total_following
        context['following'] = following
        context['followed'] = followed
        context['post_list'] = post_list
        context['fav_post'] = fav_post
        context['title'] = stuff.user.username
        context['user'] = stuff.user
        context['cat_tab'] = cat_tab
        context['notification'] = notification
        return context

class DeleteUserView(LoginRequiredMixin,DeleteView):
    model = User
    template_name = 'users/delete_user.html'
    login_url = 'login'
    redirect_field_name = 'login'
    success_url = reverse_lazy('home')

    def get_context_data(self, *args, **kwargs):
        cat_tab = Category.objects.all()[:10]
        notification = Notification.objects.filter(user=self.request.user.id) 
        context = super(DeleteUserView, self).get_context_data(*args, **kwargs)
        context["title"] = 'Delete Account'
        context['notification'] = notification
        context['cat_tab'] = cat_tab
        return context

@login_required
def FollowView(request, pk):
    profile = get_object_or_404(Profile, id=request.POST.get('profile_id'))
    pro = get_object_or_404(Profile, id=request.user.id)
    followed = False
    if profile.followers.filter(id=request.user.id).exists():
        profile.followers.remove(request.user)
        pro.following.remove(profile.user)
        followed = False
    else:
        profile.followers.add(request.user)
        pro.following.add(profile.user)
        followed = True  
        note = Notification(notification_type=3, sender=request.user, user=profile.user)
        note.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))