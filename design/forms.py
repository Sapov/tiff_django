from django import forms
from .models import OrdDesign, Comment

class AddDesignForm(forms.ModelForm):
    class Meta:
        model = OrdDesign
        fields = ['title', 'interest', 'width', 'length', 'description', 'images']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['design']