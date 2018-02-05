from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages

from .forms import BlogCategoryForm, BlogForm, CommentForm
from .models import Blog, BlogCategory, Comment

def blog_category(request):
    
    form = BlogCategoryForm(request.POST or None, prefix="create_category")
    form_blog = BlogForm(request.POST or None, prefix="create_blog")
    categories = BlogCategory.objects.all()
    blogs = Blog.objects.all()
    cxt = {
        'form':form,
        'categories':categories,
        'blogs':blogs,
        'form_blog':form_blog
    }
    if request.method == 'POST':
        if "create_category" in request.POST:
            # form = BlogCategoryForm(request.POST, prefix='create_category') 
            # if not request.user.is_staff or not request.user.is_superuser:
            #         raise Http404
            if form.is_valid():
                category = form.save(commit=False)
                category.title = form.cleaned_data['title']
                # category.user = request.user
                category.save()
                cats = Blog.objects.get(category=category.id)
                messages.success(request, "Category successfully added")
                return HttpResponseRedirect('/blog/', {'cxt':cxt, 'cats':cats})
            return HttpResponseRedirect('/blog/', {'cxt':cxt, 'cats':cats})
        # return render(request, "blog/blogview.html", cxt)

        elif "create_blog" in request.POST:
            form_blog = BlogForm(request.POST, prefix='create_blog')
            if form_blog.is_valid():
                # form_blog = BlogForm(request.POST, prefix='create_blog') 
                # import pdb; pdb.set_trace()            
                blog = form_blog.save(commit=False)
                blog.title = form_blog.cleaned_data['title']
                blog.draft = form_blog.cleaned_data['draft']
                blog.publish = form_blog.cleaned_data['publish']
                blog.content = form_blog.cleaned_data['content']
                blog.save()  
                messages.success(request, "Blog successfully added")
                return HttpResponseRedirect('/blog/', cxt)
                # return redirect('blog:hc-category', cxt)
            return HttpResponseRedirect('/blog/', cxt)
        return HttpResponseRedirect('/blog/', cxt)
    else:
        return render(request, "blog/blogview.html", cxt)

def add_comment(request, post):
    
    form_comment = CommentForm(request.POST or None)
    # form_category = BlogCategoryForm(request.POST or None, prefix='category')
    # categories = BlogCategory.objects.all()
    # blogs = Blog.objects.all()
    # blog_post = Blog.objects.get(slug=post)
    cxt = {
        'form_category':form_category,
        # 'form_comment':form_comment,
        # 'categories':categories,
        # 'blogs':blogs
    }
    if request.method == "POST":
        if "add_comment" in request.POST: 
            
            if form_comment.is_valid():
            
                comment = form_comment.save(commit=False)
                comment.body = form_comment.cleaned_data['body']
                comment.name = request.user
                comment.post_id=blog_post.id
                # blog.draft = form.cleaned_data['draft']
                comment.save()
                
                messages.success(request, "Comment successfully added")
                return redirect('blog:hc-category')
            return HttpResponseRedirect('/blog/create/', cxt)
        # return HttpResponseRedirect('/blog/', cxt)
    return render(request, "blog/view_post.html", cxt)
    


def view_blog_detail(request, slug):
    form_comment = CommentForm(request.POST or None)
    post = get_object_or_404(Blog, slug=slug)
    blog = Blog.objects.get(slug=slug)
    comments = Comment.objects.filter(post=blog.id)
    ctx = {
        'comments':comments,
        'post':post,
        'form_comment':form_comment
    }
    return render(request, "blog/view_post.html", ctx)

def edit_blog(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    form = BlogForm(request.POST or None, prefix='blog')
    cxt = {
        'form': form
    }
    if request.method == 'PUT':  
        # if not request.user.is_staff or not request.user.is_superuser:
        #         raise Http404
        if form.is_valid():
            blog = form.save(commit=False)
            blog.title = form.cleaned_data['title']
            blog.content = form.cleaned_data['content']
            blog.draft = form.cleaned_data['draft']
            blog.save()
            messages.success(request, "Blog successfully edited")
            return HttpResponseRedirect('/blog/', cxt)
        return HttpResponseRedirect('/blog/create/', cxt)
    return render(request, "blog/blog_create.html", cxt)
    return render(request, "blog/view_post.html", {'post':post} )
