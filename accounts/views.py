from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages

# Create your views here.

from django.contrib.auth.models import User

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_superuser:
                return redirect('/admin')  # Redirect to the admin dashboard
            else:
                return redirect('/normDashboard')  # Redirect to the normal user dashboard
                #return redirect('/')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                #print('Username taken')
                messages.info(request,'Username taken')
                
            elif User.objects.filter(email=email).exists():
                #print('Email taken')
                messages.info(request,'Email taken')

            else:
                user = User.objects.create_user(username=username, password=password1, email=email, 
                                                first_name=first_name, last_name=last_name)
                user.save()
                #print('User created successfully')
                messages.success(request, 'User created successfully')
                #return redirect('/')
                return redirect('login')
        else:
            #print('Passwords do not match')
            messages.error(request, 'Password do not match')

        return redirect('register')
    else:
        return render(request, 'register.html')
    

def logout(request):
    auth.logout(request)
    return redirect('/')
