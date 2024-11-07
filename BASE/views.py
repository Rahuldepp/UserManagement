from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from . models import*
from django.contrib import messages
from AUTH.views import *

def home(request):
    user_obj=User.objects.all()
   

    return render(request, 'home.html',{'users':user_obj})
@login_required
def owner_director_view(request):
    user_obj=User.objects.all()
     
    return render(request, 'owner_director_view.html',{'users':user_obj})

@login_required
def delete_user(request,user_id):
    user_obj=User.objects.all()


    user=User.objects.get(id=user_id)
    print(user.first_name)
    user.delete()
    return redirect('/owner_director_view/',{'users':user_obj})
    
def user_creation_owner(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email').lower()
        password = request.POST.get('password1')
         
        mobile_number=request.POST.get('mobile_number')
        whatsapp_number=request.POST.get('whatsapp_number')
        company_name=request.POST.get('company_name')
        registration_no=request.POST.get('registration_no')
        vat_no=request.POST.get('vat_no')
        address=request.POST.get('address')
        role=request.POST.get('role')
        designation=request.POST.get('designation')
         
        # check strong password
        check_strong=check_password_strength(password)
        if not check_strong:
             messages.error(request,"Please provide a strong password" )
             return redirect('/user_creation_owner/')


        print(email,mobile_number)
        
        print(first_name, email, password,role)
        try:
            if User.objects.filter(mobile_number=mobile_number).exists():
                messages.error(request, "This mobile_number already exists")
                return redirect('/user_creation_owner/')

            if User.objects.filter(email=email).exists():
                messages.error(request, "This email already exists")
                return redirect('/user_creation_owner/')

            # create a new user
             
            user_obj = User(first_name=first_name,last_name=last_name,email=email,mobile_number=mobile_number,whatsapp_number=whatsapp_number,company_name=company_name,registration_no=registration_no,vat_no=vat_no,address=address,role=role,designation=designation)
            user_obj.set_password(password)
            user_obj.is_verified=True
            user_obj.save()
            return redirect('/owner_director_view/')    

        except Exception as e:
            print(e)
    
    return render(request,'user_creation_owner.html')