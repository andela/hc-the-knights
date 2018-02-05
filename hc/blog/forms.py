from django import forms
from .models import BlogCategory, Blog, Comment

class BlogCategoryForm(forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ('title',)

class BlogForm(forms.ModelForm):
    # title = forms.CharField(max_length=100, required=True)
    # content = forms.CharField(max_length=500, required=True)
    class Meta:
        model = Blog
        fields = ('category', 'title','content', 'draft',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
