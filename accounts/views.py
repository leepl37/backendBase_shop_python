# Create your views here.
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from accounts.serializers import SignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404, RetrieveAPIView
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.views import LoginView as LV, logout_then_login, PasswordChangeView as AuthPasswordChangeView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from accounts.models import Profile
from django.shortcuts import render, redirect
from accounts.form import SignupForm, PasswordChangeForm, ProfileEditForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.urls import reverse_lazy
# Create your views here.


def root(request):
    return render(request, 'root.html')


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, "회원가입을 축하합니다.")
            # return render(request, 'accounts/root.html')
            return redirect('accounts:root')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {
        'form': form
    })


class LoginView(LV):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        messages.success(self.request, "로그인되었습니다.")
        return redirect('accounts:root')


login = LoginView.as_view()


def logout(request):
    messages.success(request, "로그아웃되었습니다.")
    return logout_then_login(request)


class PasswordChangeView(AuthPasswordChangeView):
    success_url = reverse_lazy('accounts:root')
    template_name = "accounts/passwordchange.html"
    form_class = PasswordChangeForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "비밀번호가 변경되었습니다.")
        return super().form_valid(form)


passwordchangeview = PasswordChangeView.as_view()


def profile(request):
    return render(request, 'accounts/profile.html')


def profilechange(request):
    if request.method == "POST":
        form = ProfileEditForm(
            request.POST, request.FILES, instance=request.user)
        form.save()
        messages.success(request, "프로필정보가 변경되었습니다.")
        return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/profilechange.html', {
        "form": form,
    })


# 회원가입 API
# settings.AUTH_USER_MODEL


class SignupView(CreateAPIView):  # CreateAPIView는 get method는 not allowed/ POST is allowed
    # model = get_user_model()
    model = Profile     # ->  settings.AUTH_USER_MODEL
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]


# 개인 프로필 API
