from django.shortcuts import render
import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from BASE.models import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import re
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout





#check for valid phone number

def is_valid_phone_number(phone_no):
    return bool(re.fullmatch(r'\d{10}', phone_no))


# for email login
def login_user(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input').lower()
        password = request.POST.get('password')
        print(user_input, password)   
         
    try:

        if (is_valid_phone_number(user_input)):
            print('phone no done')
            user_obj = User.objects.get(mobile_number=user_input)
            if user_obj is None:
                messages.error(request, 'This email does not exist ')
                return redirect('/authentication/login')
            email=user_obj.email
        else:
            print('email done')
            user_obj = User.objects.filter(email=user_input).exists()
            email=user_input
            print(user_obj)
            if user_obj is None:
                    messages.error(request, 'This email does not exist ')
                    return redirect('/authentication/login')
        if user_obj is None:
            messages.error(request, 'This email does not exist ')
            return redirect('/authentication/login')

        get_user = User.objects.get(email=email)
        if not get_user.is_verified:
            messages.error(request, 'Please verify your email first.')
            return redirect('/authentication/login')

        user = authenticate(request, email=email, password=password)
        print('email is required')
        print(user, get_user.password)
        if user is None:
            messages.error(request, 'Wrong password')
            return redirect('/authentication/login')
        else:
            login(request, user)
            is_owner = request.user.role in ['Owner', 'Director']  
            if is_owner:
                 return redirect('/owner_director_view/',{'user': user})
            return redirect('/', {'user': user,'is_owner': is_owner})
    except Exception as e:
        messages.error(request,e)
    return render(request, 'login_email.html')

def logout_user(request):
    logout(request)
    return render(request,'home.html') 
# def login_user(request):
#     if request.method == 'POST':
#         email = request.POST.get('email').lower()
#         password = request.POST.get('password')
#         print(email, password)
#     # try:
#         user_obj = User.objects.filter(email=email).exists()
#         
#         if user_obj is None:
#             messages.error(request, 'This email does not exist ')
#             return redirect('/authentication/login')
# 
#         get_user = User.objects.get(email=email)
#         if not get_user.is_verified:
#             messages.error(request, 'Please verify your email first.')
#             return redirect('/authentication/login')
# 
#         user = authenticate(request, email=email, password=password)
#         print('email is required')
#         print(user, get_user.password)
#         if user is None:
#             messages.error(request, 'Wrong password')
#             return redirect('/authentication/login')
#         else:
#             login(request, user)
#             is_owner = request.user.role in ['Owner', 'Director']  
#             if is_owner:
#                  return redirect('/owner_director_view/',{'user': user})
#             return redirect('/', {'user': user,'is_owner': is_owner})
#     # except Exception as e:
#         # messages.error(request,e)
#     return render(request, 'login_email.html')
# 
# def logout_user(request):
#     logout(request)
#     return render(request,'home.html') 
 
# register a user ------

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email').lower()
        password = request.POST.get('password1')
        cnf_password = request.POST.get('password2')
        mobile_number=request.POST.get('mobile_number')
        whatsapp_number=request.POST.get('whatsapp_number')
        company_name=request.POST.get('company_name')
        registration_no=request.POST.get('registration_no')
        vat_no=request.POST.get('vat_no')
        address=request.POST.get('address')
        role=request.POST.get('role')
        designation=request.POST.get('designation')
        if password != cnf_password:
             messages.error(request, "Your password and CNF password are not the same")
             return redirect('/authentication/register')
        check_strong=check_password_strength(password)
        if not check_strong:
             messages.error(request,"Please provide a strong password" )
             return redirect('/authentication/register')


        print(email,mobile_number)
        
        print(first_name, email, password,role)
        try:
            if User.objects.filter(mobile_number=mobile_number).exists():
                messages.error(request, "This user already exists")
                return redirect('/authentication/register')

            if User.objects.filter(email=email).exists():
                messages.error(request, "This email already exists")
                return redirect('/authentication/register')

            # create a new user
            otp=random.randint(100000,999999)
            user_obj = User(first_name=first_name,last_name=last_name,email=email,mobile_number=mobile_number,whatsapp_number=whatsapp_number,company_name=company_name,registration_no=registration_no,vat_no=vat_no,address=address,role=role,designation=designation,otp=otp,)
            user_obj.set_password(password)
            user_obj.save()

            send_mail_for_registration(email,otp)
            return redirect('/authentication/mail_send')

        except Exception as e:
            print(e)
    return render(request, 'register.html')


def verify_email_otp(request):
    if request.method=='POST':
     email=request.POST.get('email').lower()
     otp=request.POST.get('otp')
     
    try:
        if User.objects.filter(email=email).exists():
            user_obj=User.objects.get(email=email)
            user_otp=user_obj.otp
            # print(user_otp)
            if user_otp==otp:
              print(user_obj.is_verified)
              user_obj.is_verified=True               
              print(user_otp)
              user_obj.save()
              messages.success(request,"Your account has been verified")
            else:
             messages.error(request,"Please enter correct OTP")

        else:
            messages.error(request,"this email does not exist")
    except Exception as e:
            messages.error(request,e)


    return render(request, 'mail_send.html')



def success(request):
    return render(request, 'success.html')

# send mail------
def send_mail_for_registration(email, otp):
    subject = 'Hay account need to be verified'
    message = f' HI Enter this {otp} to verify your email address'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


 
    
 



# For forgot password ---------
    
def forgot_email_password(request):
   if request.method == 'POST':
     email=request.POST.get('email')
     user=User.objects.filter(email=email).first()    
     if user is None : 
         messages.error(request,'This email does not exist')
         return redirect('/authentication/register')
     if not user.is_verified:
         messages.error(request,'Please verify your email address')
         return redirect('/authentication/mail_send')
     try:
          new_otp=random.randint(100000,999999)
          user.otp=new_otp
          user.save()
          send_mail_for_newPassword(email, new_otp)
         
          return redirect('/authentication/update_email_password')

     except Exception as e:
         messages.error(request,'Something went wrong')
   return render(request,'forgot_email_password.html')


def update_email_password(request):
    if request.method=='POST':
     email=request.POST.get('email').lower()
     otp=request.POST.get('otp')
     print(email)
     password=request.POST.get('password')
     check_strong=check_password_strength(password)
     if not check_strong:
            messages.error(request,"Please provide a strong password" )
             
            return render(request, 'update_email_password.html')
     
    try:
        if User.objects.filter(email=email).exists():
            user_obj=User.objects.get(email=email)
            user_otp=user_obj.otp
            user_otp = str(user_obj.otp)
            otp = str(otp)
            print(type(user_otp))
            print("++")
            print(type(otp))
            print("--")
            print(user_otp,"->",otp)
            
            # print(user_otp)
            if user_otp==otp:
               
              user_obj.set_password(password)               
              print('password changed')
              user_obj.save()
              messages.success(request,"Your password has been changed") 
              print("password updated successfully")   
              return redirect('/authentication/login')
            else:
             messages.error(request,"Please enter correct OTP")

        else:
            messages.error(request,"this email does not exist")
    except Exception as e:
            messages.error(request,e)


    return render(request, 'update_email_password.html')

     
# send email for new password --->

def send_mail_for_newPassword(email, otp):
    subject = 'Regarding Forgot  password'
    message = f'Hi use this otp {otp} to change your password'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


# to check strong password ------>
def check_password_strength(password):
     
    if len(password) < 8:
        return False

    
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False

    
    if not re.search(r"\d", password):
        return False

     
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False

     
    return True

 


