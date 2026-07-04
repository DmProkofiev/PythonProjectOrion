from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

from users.forms import UserRegistrationForm, UserUpdateForm


# DmitriiProkofiev
# 9532607a

# вход
def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            error = "Неверный логин или пароль"
    return render(request, "users/login.html", context={"error": error})

# выход
def logout_view(request):
    logout(request)
    return redirect('index')

# регистраци
def register_view(request):
    if request.method=='POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, "users/account.html", context=context)

# заблокировать пользавателя
def bann_up_user_view(request):
    pass

# разблокировать польазвпателя
def bann_down_user_view(request):
    pass


def account_view(request):
    if request.method=="POST":
        form = UserUpdateForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            form.save()

    form = UserUpdateForm(instance=request.user)
    context = {'form': form}
    return render(request, "users/account.html", context = context)