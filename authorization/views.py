from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignupForm


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def form_invalid(self, form):
        for errors in form.errors.values():
            for error in errors:
                messages.warning(self.request, error)

        return super().form_invalid(form)


class CustomLoginView(LoginView):

    def form_invalid(self, form):
        for errors in form.errors.values():
            for error in errors:
                messages.warning(self.request, error)

        return super().form_invalid(form)

