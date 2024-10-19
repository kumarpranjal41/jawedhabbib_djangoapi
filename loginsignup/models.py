from django.db import models

# Create your models here.

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    email = models.EmailField(max_length=50 , unique=True)
    phone = models.CharField(max_length=12 , unique=True)
    location = models.CharField(max_length=100)
    gender = models.CharField(max_length=50 , choices=(
        ('Male' , 'Male') ,  ('Female' , 'Female') , ('Other' , 'Other'))
        )
    password = models.CharField(max_length=100 ,null=False ,  default='password')
    conformpassword = models.CharField(max_length=100 ,null= False ,  default='password')
    admin = models.BooleanField(default=False)
    account_created_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    

# coupons model 

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    description  = models.TextField()
    minammount  = models.TextField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    
    # ForeignKey to link coupons to a specific user
    user = models.ForeignKey(User, related_name='coupons', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.coupon_code} - {self.user.name}"



