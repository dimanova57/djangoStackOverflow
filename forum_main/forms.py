from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django import forms
from .models import Question, Answer, UserPost


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'category']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

        widgets = {'text': forms.Textarea(attrs={'class': 'form-control', 'rows': "1"})}


class PostForm(forms.ModelForm):
    class Meta:
        model = UserPost
        fields = ['title', 'text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
