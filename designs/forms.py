from django import forms
from .models import Project, Design, Comment

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'designer']

class DesignerForm(forms.ModelForm):
    class Meta:
        model = Design
        fields = ['image']

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

