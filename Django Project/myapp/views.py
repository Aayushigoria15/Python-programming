from django.shortcuts import render
from .models import Contact,User
from django.core.mail import send_mail
from django.conf import settings
import random

# Create your views here.
def index(request):
    print("Index")
    return render(request,'index.html')

def contact(request):
    if request.method=="POST":
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            mobile=request.POST['mobile'],
            remarks=request.POST['remarks']
        )
        msg=" Contact Saved Successfully!!! "
        contacts=Contact.objects.all().order_by("-id")[:3]
        return render(request,'contact.html',{'msg':msg , 'contacts':contacts})
    else:
        contacts=Contact.objects.all().order_by("-id")[:3]
        return render(request,'contact.html',{'contacts':contacts})

def signup(request):
    if request.method=="POST":
        try:
            User.objects.get(email=request.POST['email'])
            msg="Email Already Registered!!!"
            return render(request,'signup.html',{'msg':msg})
        except:
            if request.POST['password']==request.POST['cpassword']:

                User.objects.create(
                    fname=request.POST['fname'],
                    lname=request.POST['lname'],
                    email=request.POST['email'],
                    mobile=request.POST['mobile'],
                    address=request.POST['address'],
                    password=request.POST['password'],
                )
                msg="User Signup Successfully!!! "
                return render(request,'signup.html',{'msg':msg})
            else:
                msg="Password & Confirm Password Does not Match!!" 
                return render(request,'signup.html',{'msg':msg})  
    else:
        return render(request,'signup.html')

def login(request):
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            if user.password==request.POST['password']:
                request.session['email']=user.email
                request.session['fname']=user.fname
                return render(request,'index.html')

            else:
                msg="Incorrect Password!!"
                return render(request,'login.html',{'msg': msg})
        except:
            msg="Email Not Registered!!"
            return render(request,'login.html',{'msg': msg})
    else:
        return render(request,'login.html')

def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        msg="Logged out Successfully!!"
        return render(request,'login.html',{'msg': msg})
    except:
        msg="Logged out Successfully!!"
        return render(request,'login.html',{'msg': msg})

def change_password(request):
    if request.method=="POST":
        user=User.objects.get(email=request.session['email'])
        if user.password==request.POST['old_password']:
            if request.POST['new_password']==request.POST['cnew_password']:
                if user.password!=request.POST['new_password']:
                   user.password=request.POST['new_password']
                   user.save()
                   del request.session['email']
                   del request.session['fname']
                   msg="Password Change Successfully!!"
                   return render(request,'login.html',{'msg': msg})
                else:
                     msg="Your new password can't be from your old password!!"
                     return render(request,'change-password.html',{'msg': msg})
            else:
                 msg="Your new password and confirm new password does not match!!"
                 return render(request,'change-password.html',{'msg': msg})
        else:
             msg="Your old password does not match!!"
             return render(request,'change-password.html',{'msg': msg})
    else:
        return render(request,'change-password.html')
    
def profile(request):
    user=User.objects.get(email=request.session['email'])
    if request.method=="POST":
        user.fname=request.POST['fname']
        user.lname=request.POST['lname']
        user.mobile=request.POST['mobile']
        user.address=request.POST['address']
        user.save()
        msg="Profile Updated Successfully!!"
        return render(request,'profile.html',{'user': user,'msg':msg})
    else:
        return render(request,'profile.html',{'user': user})

def forgot_password(request):
    print("Forgot Password")
    if request.method=="POST":
        try:
            user=User.objects.get(email=request.POST['email'])
            otp=random.randint(1000,9999)
            context = {}
            address = request.POST['email']
            subject = 'OTP For Forgot Password'
            message = 'Your Otp for forgot password is ' +str(otp)

            if address and subject and message:
                try:
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [address,])
                    context['result'] = 'Email sent successfully'
                    request.session['otp']=otp
                    request.session['email1']=request.POST['email']
                except Exception as e:
                    context['result'] = f'Error sending email: {e}'
            else:
                context['result'] = 'All fields are required'
            
            return render(request, "otp.html", context)
        except Exception as e:
            print("Hello")
            print(e)
            msg= "Email not registered"
            return render(request,'forgot-password.html',{'msg':msg})
    else:
        return render(request,'forgot-password.html')
    
def verify_otp(request):
    otp1=int(request.session['otp'])
    otp2=int(request.POST['otp'])
    if otp1==otp2:
        del request.session['otp']
        return render (request,'new-password.html',{'msg':'please set your new password'})
    else:
        return render (request,'otp.html',{'msg':'Invalid OTP'})


def new_password(request):
    if request.POST['new_password']==request.POST['cnew_password']:
        user=User.objects.get(email=request.session['email1'])
        if user.password!=request.POST['new_password']:
            user.password=request.POST['new_password']
            user.save()
            msg="Password updated successfully" 
            del request.session['email1']
            return render(request,'login.html',{'msg': msg})
        else:
            msg="Your new password can't from your old password"
            return render(request,'new-password.html',{'msg': msg})
    else:
        msg="New password and Confirm new password does not match"
        return render(request,'new-password.html',{'msg': msg})
