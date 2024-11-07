from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, mobile_number, password=None, **extra_fields):
        if not email and not mobile_number:
            raise ValueError('The Email or Mobile Number is required to create an account')
        
        email = self.normalize_email(email)
        user = self.model(email=email, mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, mobile_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True, blank=False)
    mobile_number = models.CharField(max_length=10, unique=True, blank=False)
    whatsapp_number = models.CharField(max_length=10, blank=True)
    company_name = models.CharField(max_length=50)
    registration_no = models.CharField(max_length=50)
    vat_no = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    role = models.CharField(
        max_length=50,
        choices=[
            ('Owner', 'Owner'), 
            ('Director', 'Director'), 
            ('Finance Manager', 'Finance Manager'), 
            ('General Manager', 'General Manager')
        ]
    )
    designation = models.CharField(max_length=50)
    otp = models.CharField(max_length=6, default=None, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)  # Required by PermissionsMixin
    is_active = models.BooleanField(default=True)  # Required field to mark active users

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['mobile_number']

    objects = UserManager()

    def save(self, *args, **kwargs):
        # Assign permissions to Owner and Director roles
        super().save(*args, **kwargs)
        if self.role in ['Owner', 'Director']:
            content_type = ContentType.objects.get_for_model(User)
            add_user_perm = Permission.objects.get(codename='add_user', content_type=content_type)
            delete_user_perm = Permission.objects.get(codename='delete_user', content_type=content_type)
            self.user_permissions.add(add_user_perm, delete_user_perm)




# rahul@gmail.com{rahul}
#usermanager@gmail.com{Usermanager}
#

#rahulK@123