from math import ceil
from pyexpat.errors import messages

from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from app.models import Question, Profile, Like, Tag, Answer
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_protect
from django.forms import model_to_dict
from django.urls import reverse
from app.forms import LoginForm, RegisterForm, SettingsForm, QuestionForm
from django.contrib import messages
from django.db.models import Count, Q
from django.contrib.auth.models import User

# Create your views here.
QUESTIONS = [
    {
        'id': i,
        'title': f'Зачем мне твои яхты? {i}',
        'content': f'Я в своем познании настолько преисполнился, что я как будто бы уже сто '
                   f'триллионов миллиардов лет проживаю на триллионах и триллионах таких же '
                   f'планет, как эта Земля, мне этот мир абсолютно понятен, и я здесь ищу только одного '
                   f'- покоя, умиротворения и вот этой гармонии, от слияния с бесконечно вечным, от созерцания '
                   f'великого фрактального подобия и от вот этого замечательного всеединства '
                   f'существа, бесконечно вечного, куда ни посмотри, хоть вглубь - бесконечно'
                   f', хоть ввысь - бесконечное большое, понимаешь? {i}',
        'likes': 0,
        'tags': ['Elf', 'valli'],
        'answers_count': 0
    } for i in range(100)
]


def paginate(objects, page, per_page=5):
    paginator = Paginator(objects, per_page)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def index(request):
    page = request.GET.get('page', 1)
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, page)})


@login_required
def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    question.likes = question.like_set.filter(value=1).count()
    question.dislikes = question.like_set.filter(value=-1).count()

    if request.method == 'POST':
        answer_text = request.POST.get('answerText')
        answer = Answer.objects.create(user=request.user, question=question, text=answer_text)

        answer_count = question.answers.count()
        page_number = ceil(answer_count / 5)

        return redirect(f'/question/{question_id}?page={page_number}#answer-{answer.id}')

    answers_list = question.answers.all().annotate(
        likes=Count('like', filter=Q(like__value=1)),
        dislikes=Count('like', filter=Q(like__value=-1))
    )

    paginator = Paginator(answers_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'question.html', {'question': question, 'page_obj': page_obj})


@csrf_protect
def log_in(request):
    print(request.GET)
    print(request.POST)
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            print(user)
            if user is not None:
                login(request, user)
                print('Successfully logged in')
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, 'Wrong password or user does not exist')
    return render(request, 'login.html', context={'form': login_form})


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@csrf_protect
def signup(request):
    if request.method == 'GET':
        register_form = RegisterForm()
    elif request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # Создание и сохранение нового пользователя
            user = register_form.save()

            # Создание профиля пользователя
            Profile.objects.create(user=user)

            # Автоматический вход пользователя в систему
            login(request, user)

            # Успешное сообщение
            messages.success(request, 'Successfully signed up and logged in')

            # Редирект на исходную страницу или на главную страницу
            return redirect(request.GET.get('next', reverse('index')))
        else:
            # Отображение ошибок при неправильной валидации формы
            messages.error(request, 'Registration error')

    return render(request, 'signup.html', {'form': register_form})


@login_required(login_url='login/', redirect_field_name='continue')
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()

            tags_str = form.cleaned_data.get('tags', '')
            if tags_str:
                tag_names = [name.strip() for name in tags_str.split(',')]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    question.tags.add(tag)

            return redirect('question', question_id=question.id)
        else:
            return render(request, 'ask.html', {'form': form})
    else:
        form = QuestionForm()

    return render(request, 'ask.html', {'form': form})


@csrf_protect
@login_required(login_url='login/', redirect_field_name='continue')
def settings(request):
    if request.method == 'GET':
        settings_form = SettingsForm(initial=model_to_dict(request.user))
        return render(request, 'settings.html', context={'form': settings_form})

    elif request.method == 'POST':
        settings_form = SettingsForm(request.POST, request.FILES, instance=request.user)

        if settings_form.is_valid():
            settings_form.save()

    else:
        settings_form = SettingsForm()

    return render(request, 'settings.html', context={'form': settings_form})


@login_required(login_url='login/', redirect_field_name='continue')
def best(request):
    questions = Question.objects.top_rated_questions().annotate(
        likes=Count('like', filter=Q(like__value=1)),
        dislikes=Count('like', filter=Q(like__value=-1))
    )
    page = request.GET.get('page', 1)
    page_obj = paginate(questions, page, per_page=5)

    return render(request, 'best.html', {'page_obj': page_obj})


@login_required(login_url='login/', redirect_field_name='continue')
def new(request):
    questions = Question.objects.recent_questions()[:20].annotate(
        likes=Count('like', filter=Q(like__value=1)),
        dislikes=Count('like', filter=Q(like__value=-1))
    )
    page = request.GET.get('page', 1)
    page_obj = paginate(questions, page, per_page=5)

    return render(request, 'new.html', {'page_obj': page_obj})


@login_required(login_url='login/', redirect_field_name='continue')
def tag(request, tag_name):
    questions = Question.objects.get_by_tags(tag_name).annotate(
        likes=Count('like', filter=Q(like__value=1)),
        dislikes=Count('like', filter=Q(like__value=-1))
    )
    page = request.GET.get('page', 1)
    page_obj = paginate(questions, page)

    return render(request, 'tag.html', {'tag': tag_name, 'page_obj': page_obj})
