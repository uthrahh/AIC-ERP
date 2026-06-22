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
from django.contrib.auth import logout
from accounts.forms import ApplicantRegistrationForm
from django.contrib.auth import login
from django.contrib.auth import login


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):

        user = form.get_user()

        log_action(
            user,
            'login',
            'accounts',
            user.pk,
            request=self.request
        )

        response = super().form_valid(form)

        if user.is_admin:
            return redirect('portal:admin_home')

        elif user.is_mentor_user:
            return redirect('mentors:home')

        elif user.is_startup_user:
            return redirect('portal:startup_home')
        
        elif user.is_applicant:
            return redirect('applications:submit')

        return response

class UserLogoutView(View):

    def get(self, request):

        if request.user.is_authenticated:
            log_action(
                request.user,
                'logout',
                'accounts',
                request.user.pk,
                request=request
            )

        logout(request)

        return redirect('accounts:login')


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

def applicant_register(request):

    if request.method == "POST":

        form = ApplicantRegistrationForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            return redirect(
                "applications:submit"
            )

    else:
        form = ApplicantRegistrationForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )

def save(self, commit=True):

    user = super().save(commit=False)

    user.username = self.cleaned_data["email"]
    user.email = self.cleaned_data["email"]
    user.role = User.Role.APPLICANT

    if commit:
        user.save()

    return user