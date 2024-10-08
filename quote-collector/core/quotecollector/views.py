from django.shortcuts import render,redirect
from .models import *
query = Quote.objects.all()
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        data = request.POST
    
        author = data.get('author')
        quote = data.get('quote')
        if quote == '':
            pass
        else:
            query = Quote.objects.all()
            Quote.objects.create(quote=quote, author=author,user=request.user)
        return redirect('/')

    
    return render(request,"home.html")
@login_required(login_url='/login/')
def yourQuote(request):
    query =  Quote.objects.filter(user=request.user)
    if request.GET.get('search'):
        search = request.GET.get('search')
        print(search)
        query = Quote.objects.filter(author__icontains=search)

    return render(request,"yourQuote.html",context={'quotes':query})
@login_required(login_url='/login/')
def deleteQuote(request,id):
    queryset = Quote.objects.get(id=id)
    queryset.delete()
    return redirect('/yourquotes/')
@login_required(login_url='/login/')
def updateQuote(request,id):
    queryset = Quote.objects.get(id=id)
    if request.method == 'POST':
        data = request.POST
        quote = data.get('quote')
        
        author = data.get('author')
        print(author)
        queryset.quote  = quote
        queryset.author = author
        queryset.save()
        return redirect('/yourquotes/')
    return render(request,"update.html",context={'quotes':queryset})

def register(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
    
        if User.objects.filter(username=username).exists():
            return redirect('/register/')
        else:
            user = User.objects.create(username=username)
            user.set_password(password)
            user.save()
            print(User.objects.filter(username=username))
            return redirect('/login/')
    return render(request,"register.html")
def login_fwd(request):

    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if not User.objects.filter(username=username).exists:
            return redirect('/login/')
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                return redirect('/login/')
            else:
                login(request, user)
                return redirect('/')
    return render(request,"login.html")

def logout_user(request):
    logout(request)
    return redirect('/')