from django.shortcuts import render

# Create your views here.
QUESTIONS = [
    {
        'id': i,
        'title': f'Questions {i}',
        'content': f'Long lorem ipsum {i}'
    } for i in range(10)
]


def index(request):
    return render(request, 'index.html', {'questions': QUESTIONS})


def question(request, question_id):
    item = QUESTIONS[question_id]
    return render(request, 'question.html', {'question': item})
