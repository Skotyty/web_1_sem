from django.shortcuts import render
from django.core.paginator import Paginator

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
    } for i in range(2)
]

def paginate(objects, page, per_page=10):
    paginator = Paginator(QUESTIONS, per_page)
    return paginator.page(page)


def index(request):
    page = request.GET.get('page', 1)
    return render(request, 'index.html', {'questions': paginate(QUESTIONS, page)})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item})


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
