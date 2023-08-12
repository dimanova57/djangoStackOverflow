from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .service import get_filters_for_query, questions_by_query
from .forms import QuestionForm, AnswerForm, PostForm
from .models import Question, Answer, Category, UserPost


class MainPageView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        questions = questions_by_query(self.request)
        context['questions'] = questions
        return context


class CreateQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'ask_question.html'
    success_url = '/'
    login_url = '/auth/login/'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
            return super().form_valid(form)


class QuestionPageView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'question.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.question = Question.objects.get(pk=self.kwargs['pk'])
        form.save()
        return redirect(f'/question/{self.kwargs["pk"]}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = Question.objects.get(pk=self.kwargs['pk'])
        context['answers'] = Answer.objects.filter(question=self.kwargs['pk'])
        return context


class CategoriesPageView(TemplateView):
    template_name = 'categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class UserPageView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'
    login_url = '/auth/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        context['questions'] = Question.objects.filter(author=user)
        context['answers'] = Answer.objects.filter(author=user)

        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = UserPost
    form_class = PostForm
    template_name = 'ask_question.html'
    success_url = '/'
    login_url = '/auth/login/'

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.author = self.request.user
            return super().form_valid(form)


class PostAllPageView(TemplateView):
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = UserPost.objects.filter()
        return context


class PostPageView(CreateView):
    model = UserPost
    form_class = PostForm
    template_name = 'post.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = UserPost.objects.get(pk=self.kwargs['pk'])
        form.save()
        return redirect(f'/post/{self.kwargs["pk"]}')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = UserPost.objects.get(pk=self.kwargs['pk'])
        return context


def edit_record(request, record, record_id):
    model = Question if record == 'question' else Answer
    form_class = QuestionForm if record == 'question' else AnswerForm

    record = get_object_or_404(model, pk=record_id)

    if request.method == 'POST':
        form = form_class(request.POST, instance=record)
        if form.is_valid():
            form.save()
            return redirect('/profile')
    form = form_class(instance=record)
    return render(request, 'edit.html', {'form': form})


def delete_record(request, record, record_id):
    model = Question if record == 'question' else Answer
    obj = get_object_or_404(model, pk=record_id)

    if request.method == 'POST':
        obj.delete()
        return redirect('/profile')

    return render(request, 'delete.html', {"record": record, 'obj': obj})
