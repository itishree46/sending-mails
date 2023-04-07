from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')
def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        UFD=UserForm(request.POST)
        PFD=ProfileForm(request.POST,request.FILES)
        if UFD.is_valid() and PFD.is_valid():
            UFO=UFD.save(commit=False)
            password=UFD.cleaned_data['password']
            UFO.set_password(password)
            UFO.save()

            PFO=PFD.save(commit=False)
            PFO.profile_user=UFO
            PFO.save()

            send_mail('registration',
            'Thanks for registration,ur registration is Successfull',
            '20itishree23@gmail.com',
            [UFO.email],
            fail_silently=False
            
            )

            return HttpResponse('registration is succeffull')
    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)

        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('u r not an authenticated user')
    return render(request,'user_login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile_display(request):
    Username=request.session.get('username')
    UO=User.objects.get(username=Username)
    PO=Profile.objects.get(profile_user=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'profile_display.html',d)

@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['password']
        un=request.session.get('username')
        uo=User.objects.get(username=un)
        uo.set_password(pw)
        uo.save()
        return HttpResponse('password changed successfully.')

    return render(request,'change_password.html')

def reset_password(request):
    if request.method=='POST':
        un=request.POST['un']
        ps=request.POST['ps']
        luo=User.objects.filter(username=un)
        if luo:
            uo=luo[0]
            uo.set_password(ps)
            uo.save()
            return HttpResponse('password reset is done')
        else:
            return HttpResponse('create an account')
                    
    return render(request,'reset_password.html')




#user check if user object is empty or not and user.is_active is a variable ,it check if user is active or not