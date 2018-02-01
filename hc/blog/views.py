from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import (get_object_or_404, redirect, render,
                              render_to_response)
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from hc.front.views import _welcome_check
from .forms import BlogCategoryForm, BlogForm, CommentForm
from .models import Blog, BlogCategory, Comment


@login_required
def blog_category(request):
    """This function holds the logic for creating blog categories and blogs"""
    form = BlogCategoryForm(request.POST or None, prefix="create_category")
    form_blog = BlogForm(request.POST or None, prefix="create_blog")
    categories = BlogCategory.objects.all()
    # blogs = Blog.objects.all()
    cxt = {
        'form':form,
        'categories':categories,
        'form_blog':form_blog
    }
    if request.method == 'POST':
        if "create_category" in request.POST:
            if form.is_valid():
                category = form.save(commit=False)
                category.title = form.cleaned_data['title']
                category.save()
                messages.success(request, "Category successfully added")
                return HttpResponseRedirect('/blog/', cxt)
            return HttpResponseRedirect('/blog/', cxt)
        elif "create_blog" in request.POST:
            form_blog = BlogForm(request.POST, prefix='create_blog')
            title = request.POST['title']
            category_input = request.POST['selectop']
            publish = request.POST['publish']
            content = request.POST['content']
            category_query = BlogCategory.objects.get(id=category_input)
            blog=Blog(title=title, content=content, publish=publish, category=category_query)
            blog.save()  
            messages.success(request, "Blog successfully added")
            return HttpResponseRedirect('/blog/', cxt)
        return HttpResponseRedirect('/blog/', cxt)
    else:
        return render(request, "blog/blogview.html", cxt)

@login_required
def create_blogs(request):
    """A function to render the template for creating blog posts"""
    form = BlogCategoryForm(request.POST or None, prefix="create_category")
    form_blog = BlogForm(request.POST, prefix='create_blog')
    return render(request, 'blog/category.html', {'form':form, 'form_blog':form_blog})

def blog_by_category(request, category):
    """This function displays blogs under a specific category"""
    category = BlogCategory.objects.get(id=category)
    blogs = Blog.objects.filter(category=category)
    blogs_list = list(blogs)
    categories_list = BlogCategory.objects.all()
    paginator = Paginator(categories_list, 10)
    page = request.GET.get('page')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        categories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        categories = paginator.page(paginator.num_pages)
    paginator_blog = Paginator(blogs_list, 10)
    page = request.GET.get('page')
    try:
        blogs = paginator_blog.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator_blog.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator_blog.page(paginator.num_pages)
    if blogs:
        cxt = {
            "blogs": blogs,
            'categories':categories,
            "category": category.title
        }
        return render(request, "blog/blogview.html", cxt)
    return redirect("blog:hc-category")

@login_required
def add_comment(request, post):
    """This function holds the logic for adding comments to blog posts""" 
    form_comment = CommentForm(request.POST or None)
    comments_list = Comment.objects.all()
    paginator = Paginator(comments_list, 3)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)
    cxt = {
        'form_comment':form_comment,
        'comments':comments
    }
    blog = Blog.objects.get(id=post)
    if request.method == "POST":
        if "add_comment" in request.POST: 
            if form_comment.is_valid():
                comment = form_comment.save(commit=False)
                comment.body = form_comment.cleaned_data['body']
                comment.name = request.user
                comment.post = blog
                form_comment.save()
                messages.success(request, "Comment successfully added")
                return redirect('blog:hc-view-blog', blog.slug)
            return render(request, "blog/view_post.html", cxt)
    return render(request, "blog/view_post.html", cxt)
    
def view_blog_detail(request, slug):
    """This function displays a single blog and the comments associated with it"""
    form_comment = CommentForm(request.POST or None)
    tweet_url = 'http://localhost:8000/blog/view/'
    blog = Blog.objects.filter(slug=slug).first()
    comments_list = Comment.objects.filter(post=blog)
    paginator = Paginator(comments_list, 5)
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        comments = paginator.page(paginator.num_pages)
    ctx = {
        'comments':comments,
        'form_comment':form_comment,
        'blog':blog,
        'post':blog.id,
        'slug': blog.slug,
        'tweet_url': tweet_url,    
    }
    return render(request, "blog/view_post.html", ctx)

@login_required
def edit_blog(request, slug):
    """This function enables editing of a single blog post"""
    post = Blog.objects.get(slug=slug)
    current_user = request.user
    logged_in_user = User.objects.get(pk=current_user.id)
    author=User.objects.get(username=post.author)
    if author.id == logged_in_user.id:
        if request.method == 'POST':
            if 'editblog' in request.POST:
                blog = Blog.objects.filter(slug=slug).first()
                form = BlogForm(request.POST)    
                if form.is_valid():
                    blog.category = form.cleaned_data['category']
                    blog.title = form.cleaned_data['title']
                    blog.content = form.cleaned_data['content']
                    blog.draft = form.cleaned_data['draft']
                    blog.publish = form.cleaned_data['publish']
                    blog.save()
                    messages.success(request, "Blog successfully edited")
                    return redirect('blog:hc-view-blog', blog.slug)
                return redirect('blog:hc-edit-blog', post.slug)
        else:
            form = BlogForm(instance=post)
            cxt = {
                    'form': form,
                    'slug': slug
                    }
            return render(request, "blog/blog_create.html", cxt)
    return HttpResponse('Unauthorized', status=401)

@login_required
def delete_blog(request, slug):
    """This function allows for deleting a single blog post"""
    post = get_object_or_404(Blog, slug=slug)
    if post.author == request.user.id:
        if post.author == request.user.id:
            post.delete()
            return redirect('blog:hc-category')
        return render(request, "front/about.html", {"page": "about"})
    return HttpResponse('Unauthorized', status=401)
    