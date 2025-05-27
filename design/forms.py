from django import forms
from .models import OrderDesign, Comments

class AddDesignForm(forms.ModelForm):
    class Meta:
        model = OrderDesign
        fields = ['title', 'interest', 'width', 'length', 'description', 'images']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['designs']