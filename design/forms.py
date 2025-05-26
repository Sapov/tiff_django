from django import forms
from .models import DesignOrder


class CommentForm(forms.ModelForm):
    class Meta:
        model = DesignOrder
        fields = ('__all__')
