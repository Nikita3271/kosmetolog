"""
Definition of forms.
"""
from django.db import models
from .models import Comment
from .models import Blog

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'Имя пользователя'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Пароль'}))
    
class ReviewForm(forms.Form):
    rating = forms.ChoiceField(label='Оценка', choices=[(str(i), str(i)) for i in range(1, 6)], widget=forms.RadioSelect())
    review = forms.CharField(label='Отзыв', widget=forms.Textarea(attrs={'rows': 6, 'cols': 40}))

class CommentForm (forms.ModelForm):

 class Meta:

  model = Comment # используемая модель

  fields = ('text',) # требуется заполнить только поле text

  labels = {'text': "Комментарий"} # метка к полю формы text
  
class BlogForm(forms.ModelForm):
 class Meta:
    model = Blog
    fields = ('title','text','image',)
    labels = {'title': "Загoловок", 'text': "Полное содержание",'image': "Картинка"}