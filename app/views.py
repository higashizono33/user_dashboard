from django.views.generic import ListView, CreateView, UpdateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from accounts.forms import CustomUserCreateForm
from django.contrib.auth import update_session_auth_hash
from .forms import UpdatePasswordForm, UserUpdateForm
from django.contrib import messages
from .models import Message, Comment
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

User = get_user_model()

class UserView(LoginRequiredMixin, ListView):
    login_url = 'login'
    redirect_field_name = 'login'
    template_name = 'dashboard.html'
    model = User
    paginate_by = 2

class UserCreateView(LoginRequiredMixin, CreateView):
    login_url = 'login'
    redirect_field_name = 'login'
    form_class = CustomUserCreateForm
    success_url = reverse_lazy('dashboard')
    template_name = 'create.html'

    def form_valid(self, form):
        if not self.request.user.is_staff:
            messages.error(self.request, '*You are not authorized to add a user.')
            return redirect('new')
        else:
            form.save()
        return super(UserCreateView, self).form_valid(form)

class UserEditView(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name']
    template_name = 'edit_user.html'

    def get_success_url(self):
        return reverse_lazy('edit_user', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_staff = self.request.POST['is_staff']
        form.save()
        return super(UserEditView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p_form'] = UpdatePasswordForm(self.request.user)
        return context

def password_update(request, pk):
    update_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UpdatePasswordForm(update_user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password was successfully updated!')
            return redirect('edit_user', update_user.id)
        else:
            context = {
                'object': update_user,
                'p_form': form,
                'form': UserUpdateForm(instance=update_user),
            }
        return render(request, 'edit_user.html', context) 
    return redirect('edit_user', update_user.id)

class UserDeleteView(DeleteView):
    model = User
    template_name = 'dashboard.html'
    success_url = reverse_lazy('dashboard')
    
class ProfileEditView(UpdateView):
    model = User
    fields = ['email', 'first_name', 'last_name']
    template_name = 'edit_profile.html'

    def get_success_url(self):
        return reverse_lazy('edit_profile', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['p_form'] = UpdatePasswordForm(self.request.user)
        return context

def profile_pass_update(request):
    if request.method == 'POST':
        form = UpdatePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password was successfully updated!')
            return redirect('edit_profile', request.user.id)
        else:
            context = {
                'object': request.user,
                'p_form': form,
                'form': UserUpdateForm(instance=request.user),
            }
        return render(request, 'edit_profile.html', context) 
    return redirect('edit_profile', request.user.id) 

def profile_desc_update(request):
    if request.method == 'POST':
        request.user.description = request.POST.get('description')
        request.user.save()
        return redirect('edit_profile', request.user.id) 

class ProfileView(ListView):
    model = Message
    template_name = 'profile.html'
    ordering = '-created_at'
    paginate_by = 5
    login_url = 'index'
    redirect_field_name = 'redirect_to'

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        user = get_object_or_404(User, pk=self.kwargs['user_id'])
        self.request.session['to_whom'] = self.kwargs['user_id']
        queryset = Message.objects.filter(to_whom=user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.all().order_by('-created_at')
        context['profile'] = get_object_or_404(User, pk=self.kwargs['user_id'])
        return context

def post_message(request):
    if request.method == 'POST':
        if len(request.POST['message']) < 15:
            return JsonResponse({'error': 'Please enter your message at least 15 charactors'})
        else:
            whom = get_object_or_404(User, pk=request.session['to_whom'])
            new_message = Message.objects.create(user=request.user, to_whom=whom ,message=request.POST['message'])
            html = render_to_string('partial/message.html', {'message': new_message}, request=request)
            return JsonResponse({'html': html})

def delete_message(request, message_id):
    if request.method == 'GET':
        message = get_object_or_404(Message, pk=message_id)
        message.delete()
    return JsonResponse({'delete': True})

def edit_message(request, message_id):
    if request.method == 'POST':
        if len(request.POST['message']) < 15:
            return JsonResponse({'error': 'Please enter your message at least 15 charactors'})
        else:
            message = get_object_or_404(Message, pk=message_id)
            message.message = request.POST['message']
            message.save()
            return JsonResponse({'message': message.message})

def post_comment(request, message_id):
    if request.method == 'POST':
        if len(request.POST['comment']) < 15:
            return JsonResponse({'error': 'Please enter your comment at least 15 charactors'})
        else:
            message = get_object_or_404(Message, pk=message_id)
            Comment.objects.create(message=message, user=request.user, comment=request.POST['comment'])
            comments = Comment.objects.all().order_by('-created_at')
            html = render_to_string('partial/comment.html', {'comments': comments, 'message': message}, request=request)
            return JsonResponse({'html': html})

def delete_comment(request, comment_id):
    if request.method == 'GET':
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
    return JsonResponse({'delete': True})

def edit_comment(request, comment_id):
    if request.method == 'POST':
        if len(request.POST['comment']) < 15:
            return JsonResponse({'error': 'Please enter your comment at least 15 charactors'})
        else:
            comment = get_object_or_404(Comment, pk=comment_id)
            comment.comment = request.POST['comment']
            comment.save()
            return JsonResponse({'comment': comment.comment})