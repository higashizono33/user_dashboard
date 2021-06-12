from .forms import CustomUserCreateForm
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin

User = get_user_model()

class IndexView(TemplateView):
    template_name = 'index.html'

class SignUpView(SuccessMessageMixin, CreateView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
    success_message = 'You are successfully registered. Please Login.'