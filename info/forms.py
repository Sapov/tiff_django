from django import forms


class Feedback(forms.Form):
    phone = forms.CharField(max_length=13, label="Введите телефон для связи")
    message = forms.CharField(widget=forms.Textarea(), label="Введите ваш вопрос")
