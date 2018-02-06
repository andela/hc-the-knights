from hc.test import BaseTestCase
from django.contrib.auth.models import User
from .models import Blog, BlogCategory, Comment
from django.shortcuts import reverse
from django.utils import timezone

# Create your tests here.
class BlogCategories(BaseTestCase):
    def setUp(self):
        super(BlogCategories, self).setUp()
        self.client.login(username="alice@example.org", password="password")
        self.category = BlogCategory(title='Machine Learning')
        self.category.save()
        self.blog = Blog(title='Basics', content='It is the very beginning', 
                        category=self.category)
        self.blog.save()

    def test_create_blog(self):
        url = reverse('blog:hc-category')
        data = {'selectop': ['1'], 'title': ['read'], 'content': ['read'], 'create_blog': ['']}
        response = self.client.post(url, data)
        blog = Blog.objects.filter(title='read').first()
        self.assertEqual('read', blog.title)

    def test_create_category(self):
        url = reverse('blog:hc-category')
        data = {'create_category-title': ['read'], 'create_category': ['']}
        response = self.client.post(url, data)
        category = BlogCategory.objects.filter(title='read').first()
        self.assertEqual('read', category.title)

    def test_home_page_returns_all_categories(self):
        url = reverse('blog:hc-category')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blogview.html')

    def test_view_blogs__by_category(self):
        category = BlogCategory.objects.get(title='Machine Learning')
        url = 'http://localhost:8000/blog/views/1/'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/blogview.html')

    def test_edit_blog(self):
        blog = Blog.objects.filter(title='Basics').first()
        url = reverse('blog:hc-edit-blog', kwargs={'pk':blog.id})
        data = {'category': ['1'], 'title': ['read'], 'content': ['read'], 'editblog': ['']}
        response = self.client.post(url, data)
        blogedit = Blog.objects.filter(title='read').first()
        self.assertEqual('read',blogedit.title)

    def test_delete_blog(self):
        blog = Blog.objects.filter(title='Basics').first()
        url = reverse('blog:hc-delete-blog', kwargs={'pk':blog.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 302)
    
    def test_add_comment(self):
        blog = Blog.objects.filter(title='Basics').first()
        url = reverse('blog:hc-add-comment', kwargs={'post':blog.id})
        data = {'body': ['This is a miracle'], 'post':[blog.id], 'add_comment': ['']}
        response = self.client.post(url, data)
        comment = Comment.objects.filter(body='This is a miracle').first()
        self.assertEqual('This is a miracle', comment.body)

    def test_create_blog_form_invalid(self):
        url = reverse('blog:hc-category')
        data = {'selectop': ['1'], 'title':[''], 'content': ['read'], 'create_blog': ['']}
        response = self.client.post(url, data)
        self.assertTemplateUsed(response, 'blog/create_categories_and_blogs.html')
        

    def test_create_category_form_invalid(self):
        url = reverse('blog:hc-category')
        data = {'create_category-title': [''], 'create_category': ['']}
        response = self.client.post(url, data)
        self.assertRedirects(response, '/blog/')
        self.assertEqual(response.status_code, 302)

    def test_add_comment_form_invalid(self):
        blog = Blog.objects.filter(title='Basics').first()
        url = reverse('blog:hc-add-comment', kwargs={'post':blog.id})
        data = {'body': [''], 'post':[blog.id], 'add_comment': ['']}
        response = self.client.post(url, data)
        self.assertTemplateUsed(response, "blog/view_post.html")