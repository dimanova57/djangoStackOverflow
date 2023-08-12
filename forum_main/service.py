from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q


def get_filters_for_query(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    question_filter = {}

    if query:
        question_filter = (Q(text__icontains=query) | Q(title__icontains=query))

    if category:
        question_filter['category'] = category

    return question_filter


def questions_by_query(request):
    from forum_main.models import Question

    question_filters = get_filters_for_query(request)
    if type(question_filters) == Q:
        questions = Question.objects.filter(question_filters)
    else:
        questions = Question.objects.filter(**question_filters)

    return questions
