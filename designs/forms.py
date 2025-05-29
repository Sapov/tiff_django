from django import forms
from .models import OrderDesign, Comments

class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderDesign
        fields = ['title', 'complexity', 'interest', 'is_published']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['text', 'image']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }