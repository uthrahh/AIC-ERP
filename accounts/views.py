from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from accounts.forms import LoginForm, CustomPasswordChangeForm
from audit.utils import log_action


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        user.last_login_at = timezone.now()
        user.save(update_fields=['last_login_at'])
        log_action(user, 'login', 'accounts', user.pk, request=self.request)
        if user.is_admin:
            return redirect('portal:admin_home')
        if user.is_mentor_user:
            return redirect('mentors:home')
        if user.is_startup_user:
            return redirect('portal:startup_home')
        return response


class UserLogoutView(LogoutView):
    next_page = 'portal:home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            log_action(request.user, 'logout', 'accounts', request.user.pk, request=request)
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    template_name = 'accounts/change_password.html'

    def get(self, request):
        form = CustomPasswordChangeForm(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            log_action(user, 'password_changed', 'accounts', user.pk, request=request)
            messages.success(request, 'Password updated successfully.')
            return redirect(
                'portal:startup_home' if user.is_startup_user
                else 'mentors:home' if user.is_mentor_user
                else 'portal:admin_home'
            )
        return render(request, self.template_name, {'form': form})
