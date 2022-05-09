from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegisterForm


# Create your views here
def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # user.is_superuser = True
            user.is_staff = True
            user.save()
            return redirect("landing")
    else:
        print("else ma")
        form = RegisterForm()
        # return HttpResponse('error')
    return render(response, "parking management/park_signup.html", {'form': form})


def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return redirect('index')
            # return HttpResponse('hi success,' + user.username)
        else:
            messages.error(request, 'username or password not correct.')
            return redirect('login')

    return render(request, 'parking management/park_login.html')


