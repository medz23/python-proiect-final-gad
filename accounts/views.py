from django.shortcuts import render
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from django.http import HttpResponse,JsonResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
import random

from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Comment, Notification, Profile
from .forms import CommentForm, PostForm, UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from . import forms



def home(request):
    return render(request, "accounts/index.html")


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"

@login_required
def profile(request, username=None):
    user = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=user).order_by('-id')
    post_count = post_list.count()
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'posts': posts,
        'user_id': user,
        'post_count': post_count,
    }
    template_name = 'accounts/profile.html'

    return render(request, template_name, context)

@login_required
def updateProfile(request):
    if request.method == 'POST':
        User_form = UserUpdateForm(request.POST, instance=request.user)
        Profile_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if User_form.is_valid() and ProfileForm.is_valid():
            User_form.save()
            Profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, f'Username already exists or in use!')
            return redirect('profile-update')
    else:
        User_form = UserUpdateForm(instance=request.user)
        Profile_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
            'User_form': User_form,
            'Profile_form': Profile_form,
        }
        template_name = 'accounts/update_profile.html'

        return render(request, template_name, context)


@login_required
def userFollowUnfollow(request, pk=None):
    current_user = request.user
    other_user = User.objects.get(pk=pk)

    if other_user not in current_user.profile.follows.all():
        current_user.profile.follows.add(other_user)
        other_user.profile.followers.add(current_user)

        notify = Notification.objects.create(sender=current_user, receiver=other_user, action="started following you.")

    else:
        current_user.profile.follows.remove(other_user)
        other_user.profile.followers.remove(current_user)
    return redirect('profile', username=other_user.username)


@login_required
def post_create_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author=request.user
            post.save()
            context = {'url':post.get_absolute_url()}
            return HttpResponse(json.dumps(context), content_type='application/json')

    else:
        form = PostForm()
        context = {
            'form': form,
        }
        return render(request,'accounts/post_form.html',context)


def post_detail_view(request,slug=None):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post=post
            comment.author=request.user
            comment.save()
            return redirect('accounts:post-detail', slug=post.slug)
    else:
        form = CommentForm()

        comments = Comment.objects.filter(post=post).order_by('-id')
        context = {'post':post,'form':form,'comments':comments}

    return render(request,'accounts/post_detail.html',context)


@login_required
def post_update_view(request,pk):
    post1 = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES,instance=post1)
        if form.is_valid():
            post=form.save(commit=False)
            post.author = request.user
            post.save()
            ctx = {'url':post.get_absolute_url()}
            return HttpResponse(json.dumps(ctx), content_type='application/json')
    else:
        post = get_object_or_404(Post,pk=pk)
        form = PostForm(instance = post)
        context = {
            'form': form,
            'post':post,
        }
        return render(request,'accounts/post_form_update.html',context)

@login_required
def post_delete_view(request, pk=None):
    context = {}
    post = get_object_or_404(Post,pk=pk)

    if request.method =="POST":
        if post.author == request.user:
            post.delete()
            return redirect('accounts:profile', username=request.user.username)
    context = {"post":post}
    return render(request,'accounts/post_confirm_delete.html',context)



@login_required
def search_view(request):

    message = ""
    post_list = Post.objects.all().order_by('-pk');
    page = request.GET.get('page', 1)
    paginator = Paginator(post_list, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        try:
            search_input = request.POST.get('search')
            result_posts = Post.objects.filter(Q(title_icontains=search_input)|Q(content_icontains=search_input))
            users = User.objects.filter(Q(username__iexact=search_input))

            # first condition :  users-0
            if users.count() == 0:
                message = "No results found for: " + search_input
                context = {'message':message,'posts':posts,'search_input':search_input}
                return render(request,'accounts/search.html',context)


            # second condition :user: yes
            else:
                context = {'users':users,'search_input':search_input}
                return render(request,'accounts/search.html',context)

        except:
            message = "Unexpected Error Occured!"
            context = {'message':message}
            return render(request,'accounts/search.html',context)
    else:
        flag = True
        context = {'posts':posts,'flag':flag}
        return render(request,'accounts/search.html',context)


@login_required
@require_POST
def like_view(request):
    if request.method == 'POST':
        user = request.user
        pk = request.POST.get('pk', None)
        post = get_object_or_404(Post, pk=pk)

        if post.likes.filter(id=user.id).exists():
            post.likes.remove(user)
            like = False
            post_id = '#like'+str(post.id)
        else:
            post.likes.add(user)
            like = True
            post_id = '#like'+str(post.id)

    ctx = {'likes_count': post.total_likes,'like':like,'post_id':post_id}
    return HttpResponse(json.dumps(ctx), content_type='application/json')

@login_required
def notifications_view(request,username=None):
    user = get_object_or_404(User,username=username)
    notifications = Notification.objects.filter(receiver=user).order_by('-timestamp')
    page = request.GET.get('page', 1)
    paginator = Paginator(notifications, 6)
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)

    return render(request,'accounts/notifications.html',{'notifications':notifications})

@login_required
def notifications_update_view(request,username=None):
    user = get_object_or_404(User,username=username)
    if user == request.user:
        notifications = Notification.objects.filter(receiver=user)
        for notification in notifications.all():
            if notification.read == False:
                notification.read = True
                notification.save()
        return HttpResponse('')


@login_required
def notifications_unread_count_view(request,username=None):
    user = get_object_or_404(User,username=username)
    if user == request.user:
        notifications = Notification.objects.filter(receiver=user)
        count = 0
        for notification in notifications.all():
            if notification.read == False:
                count = count+1
        data = {
            'count':count
        }
        return JsonResponse(data)
