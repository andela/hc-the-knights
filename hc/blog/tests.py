from hc.test import BaseTestCase
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
        print (category.id)
        url = 'hc-the-knight.herokuapp.com/blog/views/1/'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/blogview.html')
