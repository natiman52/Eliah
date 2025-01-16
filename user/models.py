from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models.signals import post_save,pre_delete
from django.dispatch.dispatcher import receiver
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers
# Create your models here.

def userupload(sender,file):
    return f'user/{sender.user.phone}/{file}'
class MyManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        """
        Create and save a user with the given phone and password.
        """
        if not phone:
            raise ValueError(_("The phone must be set"))
        phone = phonenumbers.parse(phone)
        user = self.model(phone=phonenumbers.format_number(phone,phonenumbers.PhoneNumberFormat.INTERNATIONAL), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, phone, password, **extra_fields):
        """
        Create and save a SuperUser with the given phone and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(phone, password, **extra_fields)

class MyUser(AbstractBaseUser,PermissionsMixin):
    phone = PhoneNumberField(null=False,blank=False,unique=True,region="ET")
    firstname =models.CharField("Firstname",max_length=50)
    lastname =models.CharField("Lastname",max_length=50)
    is_staff =models.BooleanField('staff',default=False)
    is_admin=models.BooleanField('admin',default=False)
    is_active = models.BooleanField(default=True)
    is_superuser =models.BooleanField('superuser',default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    pic = models.ImageField('profile pic',upload_to=userupload,default='user/default/profile.png')
    objects= MyManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS=[]
    def get_full_name(self):
        return f'{self.firstname} {self.lastname}'
    def __str__(self):
        return f'{self.phone}'
    
@receiver(pre_delete,sender=MyUser)
def deletePic(sender,instance,*args,**kwargs):
    if(instance.pic != "user/default/profile.png"):
        instance.pic.delete(save=True)