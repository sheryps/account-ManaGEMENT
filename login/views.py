from email.headerregistry import Address
import os
from re import M
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes,force_str
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from . forms import SignUpForm,AddUserForm,PasswordChangeForm,ResetForms,NewPasswordResetForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash
from login.models import Employeedetails, academic_details, user_details,reason,Leave,course,employee,Task
# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect(homepage)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            print('not none')
            user_block = User.objects.get(username=username)
            print(user_block)
            if user_block.is_superuser==1:
                login(request,user)
                return redirect(admin_homepage)
            else:
                if user_block.is_staff==0:
                   login(request,user)
                   return redirect(homepage)
                else:
                    messages.error(request,'user is blocked')   
        else:
            messages.error(request,'Invalid Username and Password')
            return redirect(user_login)
            
    return render(request,'userlogin.html')   
@login_required()
def homepage(request):
    if request.user.is_authenticated:
        userr=request.user
        id=request.user.id
        details = User.objects.filter(username=userr)
        images=user_details.objects.filter(user=id)
        return render(request,'home.html',{'userr':details,'images':images})
        
        
    return redirect(user_login)
@login_required()
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect(user_login)
def lohout(request):
    m =1
    m +=2
    print(M)
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit = False)
            save_form.set_password(form.cleaned_data.get('password'))
            save_form.save()
            messages.success(request, 'User registered successfully')
            return redirect(user_login)
        else:
            return render(request, 'usersignup.html', {'form':form}) 
    form = SignUpForm()
    return render(request, 'usersignup.html', {'form':form})
@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data.get('new_password'))
            user.save()
            update_session_auth_hash(request, user) #keep user logged in
            messages.success(request, 'Password changed successfully')
            return redirect('user_login')
        else:
            return render(request, 'password.html', {'form':form})

    return render(request, 'password.html')
#edit profile 
@login_required()   
def addprofile( request ):
        id = request.GET.get( 'id' )
        user = User.objects.filter( id = id )
        if user:
            profile = User.objects.get( id = id )
            ug=course.objects.all()
            images=user_details.objects.filter(user=id)
            return render(request,'userprofile.html',{ 'profile':profile,'ug':ug,'images':images})
        return redirect('home.html')
def profile(request):
    if request.method == 'POST':
       id = request.POST[ 'id' ]
       fname = request.POST[ 'fname' ]
       lname = request.POST[ 'lname' ]
       under=request.POST['under']
       mark=request.POST['mark']
       User.objects.filter( id = id ).update( first_name=fname,last_name=lname)
       idd=User.objects.get(id=id)  
       res = course.objects.get(id=under)    
       mob=request.POST['mob']
       address=request.POST['address']
       dob=request.POST['dob']
       if request.FILES.get('file') is not None:
            simage=request.FILES['file']
       else:
            simage="/static/image/default.jpg"  
       update=user_details(phone=mob,Address=address,DOB=dob,user=idd,image=simage)
       update1=academic_details(ugmark=mark,course=res,user=idd)
       update.save()
       update1.save()
       return redirect(homepage)
@login_required() 
def viewprofile(request):
    id = request.GET.get( 'id' )
    per = user_details.objects.filter( user = id )
    acd=academic_details.objects.filter(user=id)
    em=Employeedetails.objects.filter(user=id)
    images=user_details.objects.filter(user=id)
    return render(request,'viewprofile.html',{ 'pers':per,'acds':acd,'emp':em,'images':images }) 
@login_required()    
def updateprofile(request):
    id = request.GET.get( 'id' )
    user=user_details.objects.get( user = id )
    images=user_details.objects.filter(user=id)
    return render(request,'edituserprofile.html',{'user1':user,'images':images})  
@login_required()    
def edituserprofile(request):
    if request.method=='POST':
       id = request.GET.get( 'id' ) 
       fname = request.POST.get( 'fname' )
       lname = request.POST.get( 'lname' )
       User.objects.filter( id = id ).update( first_name=fname,last_name=lname)
       mob = request.POST.get( 'mob' )
       add = request.POST.get( 'add' )
       user_details.objects.filter( id = id ).update( phone=mob,Address=add)
       images=user_details.objects.get(id=id)
       if request.FILES.get('img') is not None:
           if not images.image == '/static/image/default.jpg':
                os.remove(images.image.path)
                images.image=request.FILES['img']
           else:
                print('static')
                images.image=request.FILES['img']
       else:
            print('none')
            os.remove(images.image.path)
            images.image = '/static/image/default.jpg'      
       images.save()
       return redirect(homepage)

@login_required()
def leave(request):
    id = request.GET.get( 'id' )
    user = User.objects.get( id = id )
    reasons=reason.objects.all()
    images=user_details.objects.filter(user=id)
    return render(request,'leave.html',{ 'user':user,'reasons':reasons,'images':images })
@login_required()
def insertleave(request):
    if request.method == 'POST':
       id = request.POST[ 'id' ]
       date = request.POST[ 'start' ]
       sell=request.POST['sel']
       res = reason.objects.get(id=sell)
       idd=User.objects.get(id=id)
       lve=Leave(reasondate=date,
                     reason=res,user=idd)
       lve.save()              
       return redirect('/')
@login_required()       
def viewleave(request):
        id = request.GET.get( 'id' )
        vw = Leave.objects.filter( user = id )
        images=user_details.objects.filter(user=id)
        return render(request,'viewleave.html',{ 'view':vw,'images':images })
@login_required(login_url='/')
def admin_homepage(request):
        admin_details = User.objects.filter(is_superuser=0) 
        active=User.objects.filter(is_staff=0)
        return render(request,'manageemploy.html',{ 'user' : admin_details,'active':active})

@login_required(login_url='/')
def user_edit( request ):
        id = request.GET.get( 'id' )
        user = User.objects.filter( id = id )
        employees=employee.objects.all()
        if user:
            user_details = User.objects.get( id = id )
            return render(request,'admin_userinfo.html',{ 'user':user_details,'employees':employees })
        return redirect(admin_homepage)


@login_required(login_url='/')
def user_update(request):
        if request.method == 'POST':
            id = request.POST[ 'id' ]
            desg = request.POST[ 'sell' ]
            sal = request.POST[ 'salary' ]
            res = employee.objects.get(id=desg)
            idd=User.objects.get(id=id)
            emp=Employeedetails(employee=res,salary=sal,user=idd)
            emp.save()
            return redirect(admin_homepage)

def user_block(request):
        id = request.GET.get('id')
        user = User.objects.get( id = id )
        if user.is_staff == 0:
            User.objects.filter(id=id).update(is_staff = 1)
        else:
            User.objects.filter(id=id).update(is_staff=0)

        return redirect(admin_homepage)


def user_delete(request):
        id = request.GET.get('id')
        User.objects.filter(id = id).delete()
        return redirect(admin_homepage)


@login_required(login_url='/')
def user_add(request):
        if request.method == 'POST':
            form = AddUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(admin_homepage)
            else:
                messages.error(request,'Details not valid.. ')
        form = AddUserForm()
        context = {
            'form':form
        }
        return render(request,'admin_adduser.html',context)




def searched(request):
    if request.method == 'POST':
        val = request.POST['searched']
        admin_details = User.objects.filter(username__contains=val)
        return render(request,'adminhome.html',{ 'user' : admin_details})

def leavemanager(request):
    man=Leave.objects.all()
    return render(request,'leavemanager.html',{'display':man})  

def approve(request):
    id = request.GET.get( 'id' )
    upprve = Leave.objects.filter( id = id )
    if upprve is not None:
        Leave.objects.filter(id=id).update(status='Approved')
        return redirect(leavemanager)
def reject(request):
    id = request.GET.get( 'id' )
    upprve = Leave.objects.filter( id = id )
    if upprve is not None:
        Leave.objects.filter(id=id).update(status='Rejected')
        return redirect(leavemanager)    

def taskassign(request):
    id = request.GET.get( 'id' )
    user_details = User.objects.get( id = id )
    return render(request,'task.html',{'user':user_details} )

def updatetask(request):
    if request.method == 'POST':
            id = request.POST[ 'id' ]
            start = request.POST[ 'start' ]
            end = request.POST[ 'end' ]
            work = request.POST[ 'work' ]
            idd=User.objects.get(id=id)
            task=Task(start=start,end=end,work=work,user=idd)
            task.save()
            return redirect(admin_homepage)
def taskmanager(request):
    m=Task.objects.all()    
    return render(request,'showtask.html',{'display':m})

def viewtask(request):
    id = request.GET.get( 'id' )
    vw = Task.objects.filter( user = id )
    images=user_details.objects.filter(user=id)
    return render(request,'viewtask.html',{ 'view':vw,'images':images })
def complete(request):
    id = request.GET.get( 'id' )
    upprve = Task.objects.filter( id = id )
    if upprve is not None:
        Task.objects.filter(id=id).update(status='Completed')
        return redirect(taskmanager)
def extend(request):
    id = request.GET.get( 'id' )
    ex=Task.objects.get(id=id)
    return render(request,'extend.html',{'ex':ex})
def updatedate(request):
    if request.method == 'POST':
        end = request.POST[ 'end']
        id = request.POST[ 'id' ]
        Task.objects.filter(id=id).update(end=end,status='Extended')
        return redirect(taskmanager)

def password_reset_request(request):
    if request.method == "POST":
        form = ResetForms(request.POST)
        if form.is_valid():
            gotten_email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=gotten_email)
                if user:
                    subject = "Password Reset Email"
                    email_template_name = "password_reset_email.html"
                    c = {
                    "email":user.email,
                    'domain':'localhost:8000',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER , [user.email], fail_silently=False)
                        return redirect("password_reset_done")
                    except BadHeaderError:
                        messages.error(request, 'please try again')
                        return redirect('reset_password')
                else:
                    messages.error(request, 'The email is not registered')
                    return redirect('reset_password')    
            except User.DoesNotExist:
                messages.error(request, 'The email is not registered')
                return redirect('reset_password')   

    else:
        form = ResetForms()
    return render(request, "password_reset_form.html", {"password_reset_form":form})


def password_reset_confirm(request,uidb64,token):
    user_pk = force_str(urlsafe_base64_decode(uidb64))  
    user = User.objects.get(pk=user_pk)
    if request.method == 'POST':
        form = NewPasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('password_reset_complete')
        else:
            return render(request, 'password_reset_confirm.html', {'form':form}) 
    else:
        form = NewPasswordResetForm()
    return render(request, 'password_reset_confirm.html', {'form':form}) 
