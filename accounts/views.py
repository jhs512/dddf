from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.views import (
    logout_then_login, LoginView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from lazy_string import LazyString

from .decorators import logout_required
from .forms import JoinForm, FindUsernameForm, LoginForm
from .models import User


class MyLoginView(SuccessMessageMixin, LoginView):
    template_name = "accounts/login.html"
    next_page = "/"

    form_class = LoginForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.success_message = LazyString(
            lambda: f'{self.request.user.name}님 환영합니다.')

    def get_initial(self):
        initial = self.initial.copy()
        initial['username'] = self.request.GET.get('username', None)

        return initial


@logout_required
def login(request: HttpRequest):
    return MyLoginView.as_view()(request)


def logout(request: HttpRequest):
    messages.success(request, "로그아웃 되었습니다.")
    return logout_then_login(request)


@logout_required
def join(request: HttpRequest):
    if request.method == 'POST':
        form = JoinForm(request.POST, request.FILES)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입 환영합니다.")
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = JoinForm()
    return render(request, 'accounts/join.html', {
        'form': form,
    })


def find_username(request: HttpRequest):
    if request.method == 'POST':
        form = FindUsernameForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            qs: QuerySet = User.objects.filter(email=email, name=name)

            if not qs.exists():
                messages.warning(request, "일치하는 회원이 존재하지 않습니다.")
            else:
                user: User = qs.first()
                messages.success(request, f"해당회원의 아이디는 {user.username} 입니다.")
                return redirect(reverse("accounts:login") + '?username=' + user.username)
    else:
        form = FindUsernameForm()

    return render(request, 'accounts/find_username.html', {
        'form': form,
    })
