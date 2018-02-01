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
                        category=self.category, publish='2018-02-13')
        self.blog.save()

    def test_create_blog(self):
        url = reverse('blog:hc-categories')
        data = {'title':'Computer engineering', 'content':'yes yes', 
                'category':self.category, 'publish':'2018-02-13'}
        response = self.client.post(url, data)
        category = Blog.objects.filter(title='Computer engineering').first()
        print (category)
        print ('ffffffffffff')
        self.assertEqual = ('Computer engineering', category.title)

    
