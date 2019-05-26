from django.shortcuts import render, redirect
from .models import Article, LoginForm, RegisterForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login


def archive(request):
    return render(request, 'archive.html', {"posts":Article.objects.all()})

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {        'text': request.POST["text"],
                            'title': request.POST["title"]
                            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                title=form["title"]
                # проверка на уникальность
                if not Article.objects.filter(title=title).exists():
                    article = Article.objects.create(text=form["text"],
                                       title=form["title"],
                                       author=request.user)
                    return redirect('get_article', article_id = article.id)
                else:
                    form ["errors"] = (u"Статья с таким именем уже существует")
                    return render(request, 'create_post.html', {"form": form})
            # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form ["errors"] = (u"Не все поля заполнены")
                return render(request, 'create_post.html', {"form": form})
        else:
                # просто вернуть страницу с формой, если метод GET
                return render(request, 'create_post.html', {}) 
    else:
            raise Http404


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            conpassword = form.cleaned_data.get('password')
            user = authenticate(username=user.username, emai=user.email, password=conpassword)
            login(request, user)
            return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form}) 

        

def log_in(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return HttpResponseRedirect('../../archive/')
    else:
        form = LoginForm()
    return render(request, 'user.html', {'form':form})
    
