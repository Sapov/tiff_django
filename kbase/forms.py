from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'images', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

