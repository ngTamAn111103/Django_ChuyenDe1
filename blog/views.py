# Importing necessary libraries and modules
from typing import Any
from django import http
from django.forms.models import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CommentForm, PostForm
from django.views import generic
from .models import User
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from blog.forms import UserForm,UserProfileForm


from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# View to display a list of all posts
# @staff_member_required
# Tâm An
def post_list(request):
    posts = Post.objects.filter(updated_at__isnull=False, status = "0").order_by('-updated_at')
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        post.updated_at = timezone.now()
        post.save()
        return redirect('post_list')
    return render(request, 'post_list.html', {'posts': posts})
# def post_list(request):
#     posts = Post.objects.filter(updated_at__isnull=False).order_by('-updated_at')
#     if request.method == "POST":
#         post_id = request.POST.get('post_id')
#         post = get_object_or_404(Post, pk=post_id)
#         post.updated_at = timezone.now()
#         post.save()
#         return redirect('post_list')
#     return render(request, 'post_list.html', {'posts': posts})


# Tâm An
def post_detail(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    # Query to get all comments associated with this post
    # comments = post.comment_set.all()
    # Checking if the request method is POST to process the form data
    if request.method == "POST":
        form = CommentForm(request.POST)  # Creating a form instance with the submitted data
        if form.is_valid():  # Validating the form data
            # comment = form.save(commit=False)  # Saving the form data as a comment object, but not saving to the database yet
            # comment.post = post  # Assigning the post to the comment
            # comment.author = request.user  # Assigning the logged in user as the author of the comment
            # comment.save()  # Saving the comment object to the database
            print()

    else:
        form = CommentForm()  # Creating an empty form instance if the request method is not POST
    # Rendering the template post_detail.html with the post, comments, and form data
    comments = Comment.objects.all().filter(post = pk)

    return render(request, 'post_detail.html', {'post': post, 'form': form, 'comments':comments})
# # View to display the details of a specific post
# def post_detail(request, pk):
#     # Query to get a specific post based on its primary key (pk)
#     post = get_object_or_404(Post, pk=pk)
#     # Query to get all comments associated with this post
#     # comments = post.comment_set.all()
#     # Checking if the request method is POST to process the form data
#     if request.method == "POST":
#         form = CommentForm(request.POST)  # Creating a form instance with the submitted data
#         if form.is_valid():  # Validating the form data
#             comment = form.save(commit=False)  # Saving the form data as a comment object, but not saving to the database yet
#             comment.post = post  # Assigning the post to the comment
#             comment.author = request.user  # Assigning the logged in user as the author of the comment
#             comment.save()  # Saving the comment object to the database
#     else:
#         form = CommentForm()  # Creating an empty form instance if the request method is not POST
#     # Rendering the template post_detail.html with the post, comments, and form data
#     return render(request, 'post_detail.html', {'post': post, 'form': form})

# View to add a comment on a specific post
@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)  # Redirecting back to the post detail page
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form})

# Additional views for superusers to create, edit, publish posts, and manage drafts
@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
def create_post(request):
    # Checking if the request method is POST to process the form data
    if request.method == "POST":
        form = PostForm(request.POST)  # Creating a form instance with the submitted data
        if form.is_valid():  # Validating the form data
            post = form.save(commit=False)  # Saving the form data as a post object, but not saving to the database yet
            post.author = request.user  # Assigning the logged in user as the author of the post
            post.save()  # Saving the post object to the database
            return redirect('post_detail', pk=post.pk)  # Redirecting to the post detail page after successful post creation
    else:
        form = PostForm()  # Creating an empty form instance if the request method is not POST
    # Rendering the template create_edit_post.html with the form data
    return render(request, 'create_edit_post.html', {'form': form})

@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
def edit_post(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    # Checking if the request method is POST to process the form data
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)  # Creating a form instance with the submitted data and the post instance
        if form.is_valid():  # Validating the form data
            form.save()  # Saving the form data to the database
            return redirect('post_detail', pk=post.pk)  # Redirecting to the post detail page after successful post editing
    else:
        form = PostForm(instance=post)  # Creating a form instance with the post instance if the request method is not POST
    # Rendering the template create_edit_post.html with the form data
    return render(request, 'create_edit_post.html', {'form': form})

@staff_member_required  # Decorator to ensure only staff memberfs (including superusers) can access this view
def publish_post(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    post.publish()  # Publishing the post using the publish method defined in the Post model
    return redirect('post_detail', pk=post.pk)  # Redirecting to the post detail page after successful post publishing

@staff_member_required  # Decorator to ensure only staff members (including superusers) can access this view
# Tâm An
def draft_list(request):
    # Query to get all draft posts from the database, ordered by creation date in descending order
    drafts = Post.objects.filter(updated_at__isnull=False, status = "1").order_by('-updated_at')
    # Rendering the template draft_list.html with the drafts data
    print(drafts)
    return render(request, 'draft_list.html', {'drafts': drafts})
# def draft_list(request):
#     # Query to get all draft posts from the database, ordered by creation date in descending order
#     drafts = Post.objects.filter(updated_at__isnull=True, status=1)
#     # Rendering the template draft_list.html with the drafts data
#     return render(request, 'draft_list.html', {'drafts': drafts})



@staff_member_required
def publish_post_page(request):
    drafts = Post.objects.filter(updated_at__isnull=True)
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)
        post.updated_at = timezone.now()
        post.save()
        return redirect('publish_post_page')
    return render(request, 'publish_post_page.html', {'drafts': drafts})


# login
def index(request):
    return render(request, 'post_list.html')


#trang logout
def index1(request):
    return render(request, 'post_list.html')
@login_required
def special(request):
    return HttpResponse("You are Logged in!")

@login_required
def special(request):
    return HttpResponse('You are Logged in')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('post_list'))
# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('post_list')
    
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() :
            user =  user_form.save()
            user.password = user.password
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            # if 'profile_pic' in request.FILES:
            #     profile.profile_pic = request.FILES['profile_pic']
            profile_pic = '8106194_cover-intel-socket-lga-1851-tinhte.jpg'
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request,'registration.html',{'user_form': user_form,'profile_form': profile_form ,'registered':registered   } )
# Tâm An
def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.login(username, password)
        if user is not None:
            posts = Post.objects.filter(updated_at__isnull=False, status = "0").order_by('-updated_at')
            # return render(request,'post_list.html',{'user': user, 'posts': posts} )
            return render(request,'post_list.html',{'user': user, 'posts': posts} )
        else:
            return HttpResponse("Thất bại")

        # user = User.login(username,password)
        # if user is not None:
        #     return HttpResponse('Đăng nhập thành công')
        # else:
        #     return HttpResponse('Đăng nhập thất bại')

    else:
        return render(request,'login.html',{})
# def user_login(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = User.login( username,password )
        

#         if user:
#             if user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('post_list'))
#             else:
#                 return HttpResponse('ACCOUNT NOT ACTIVE')
#         else:
#             print('soneone tried to login anh fail:')
#             print("username: {} and password: {}".format(username,password))
#             return HttpResponse("Đăng nhập thất cmn bại")
#     else:
#         return render(request,'login.html',{})
    # Tâm An
def getAllCommentsForPost(request):
    # Post_ID
    post_id = request.POST.get('post_id')
    comments = Comment.objects.filter(post_id = post_id)
    return render(request, 'post_detail.html', {'comments': comments})


class CreateNewPost(CreateView):
    model = Post
    template_name = "new_post.html"
    fields = ['title','content','categori','status']
    success_url = "/"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        obj = form.save(commit = False)
        obj.author = User.objects.get(id=self.request.user.id)
        obj.created_at = timezone.now()
        obj.thumbnail = '4572202_cover_home_air_force_one.jpg'
        obj.ụpdated_at = timezone.now()
        obj.comments = 0
        obj.likes = 0
        obj.views = 0
        obj.thumbnail = '8101948_Cover-iphone-15-pro-max-co-the-chiem-3540-lo-hang-iphone-moi-tinhte-tuanhtran.jpg'
        obj.save()
        return super().form_valid(form)

class UpdatePost(UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ['title','content','categori','status']
    success_url = "/"
class DeletePost(DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = "/"
    def tes_func(self):
        post= self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Duy: Public post
@staff_member_required  # Decorator to ensure only staff memberfs (including superusers) can access this view
def publish_post(request, pk):
    # Query to get a specific post based on its primary key (pk)
    post = get_object_or_404(Post, pk=pk)
    post.publish()  # Publishing the post using the publish method defined in the Post model
    # Tâm AN: Muốn return về index
    return redirect('post_list')  # Redirecting to the post detail page after successful post publishing

   

    