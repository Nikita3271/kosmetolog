"""
Определение представлений
"""

from .models import Comment # использование модели комментариев
from .forms import BlogForm, CommentForm # использование формы ввода комментария
from django.db import models
from .models import Blog
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from .forms import ReviewForm
def home(request):
    """Отображает домашнюю страницу"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Отображает страницу контактов"""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Страница с нашими контактами',
            'message':'',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Отображает страницу "О нас" """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'',
            'year':datetime.now().year,
        }
    )

def review(request):
    assert isinstance(request, HttpRequest)
    data = None
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = dict()
            data['rating'] = form.cleaned_data['rating']
            data['review'] = form.cleaned_data['review']
            form = None
    else:
        form = ReviewForm()
    return render(
        request,
        'app/review.html', 
        {
            'title':'Оставьте отзыв',
            'form': form,
            'data': data
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":  # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid():  # валидация полей формы
            reg_f = regform.save(commit=False)  # не сохраняем автоматически данные формы
            reg_f.is_staff = False  # запрещен вход в административный раздел
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации
            reg_f.save()  # сохраняем изменения после добавления данных
            return redirect('home')  # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных нового пользователя

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )
def news(request):
    """Отображает страницу "Страница с новостями" """
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    
    return render(
        request,
        'app/news.html',
        {
            'title':'Новости фирмы',
            'message':'',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )
def newspost(request, parametr):
    """Отображает страницу "Страница с новостями" """
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)
    
    if request.method == "POST": 
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user 
            comment_f.date = datetime.now() 
            comment_f.post = Blog.objects.get(id=parametr) 
            comment_f.save() 
            return redirect('newspost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария

    else:

         form = CommentForm() # создание формы для ввода комментария

    return render(
        request,
        'app/newspost.html',
        {
            'title': post_1.title,
            'message':' ',
            'post_1': post_1, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы
        }
    )
@login_required
def newpostblog(request):
    """Renders the new post page."""
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated and request.user.is_superuser:
        # Проверяем, аутентифицирован ли пользователь и является ли он суперпользователем
        if request.method == "POST":
            # после отправки формы
            blog_form = BlogForm(request.POST, request.FILES)
            if blog_form.is_valid():
                blog_f = blog_form.save(commit=False)
                blog_f.posted = datetime.now()
                blog_f.author = request.user
                blog_f.save()
                # сохраняем изменения после добавления полей
                return redirect('news')
                # переадресация на страницу Блог после создания статьи Блога
        else:
            blog_form = BlogForm()
            # создание объекта формы для ввода данных
        return render(
            request,
            'app/newpostblog.html',
            {'blogform': blog_form,  # передача формы в шаблон веб-страницы
             'title': 'Добавить статью блога',
             'year': datetime.now().year
             }
        )
    else:
        # Если пользователь не аутентифицирован или не является суперпользователем, перенаправляем его на другую страницу
        return redirect('home')
    
def videopost(request):
    """Отображает страницу "О нас" """
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'',
            'year':datetime.now().year,
        }
    )