from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import UserAdminCreationForm,BrandForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'base/index.html')

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request=request, username=username, password=password)

            if user is not None and user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid phone number or password')
    else:
        form = AuthenticationForm()

    context = {'forms' : form, 'page': page}
    return render(request, 'base/login.html', context)


def registerpage(req):
    form = UserAdminCreationForm()
    if req.method == 'POST':
        form = UserAdminCreationForm(req.POST)
        if form.is_valid():
            user = form.save()
            login(req, user)
            return redirect('home')
        else:
            messages.error(req, "An Error During Registration")
        
    return render(req, 'base/login.html', {'form': form})
    

def about(request):
    return render(request, "base/about.html")

def logoutpage(request):
    logout(request)

    return redirect('home')

@login_required(login_url='/login')
def add_brand(request):
    form = BrandForm(request.POST or None,  request.FILES, owner=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"forms": form}
    return render(request, 'base/add-brand.html', context)
