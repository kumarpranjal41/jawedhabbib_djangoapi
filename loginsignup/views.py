from django.shortcuts import render
from rest_framework import viewsets
from loginsignup.serializers import UserSerializer , CouponSerializer
from loginsignup.models import User , Coupon
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action



# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('account_created_date').reverse()
    serializer_class =UserSerializer


class LoginViewSet(APIView):
    def post(self , request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        if not phone or not password:
            return Response({'message': 'please enter phone and password'} , status= 400)

        try:
            user = User.objects.get(phone=phone)


            if user.password ==password:
                # token, created = Token.objects.get_or_create(user=user)
                return Response({'message' : 'login sucesfull' , 'user_id':user.pk , "admin":user.admin} , status=200)
            else:
                return Response({'message':'Incorrect Password'} , status=400)
        except User.DoesNotExist:
            return Response({'message':'user not found'} , status=404)

            

class UserCouponsView(APIView):
    def get(self, request, user_id):
        try:
            # Fetch the user based on the provided user_id
            user = User.objects.get(pk=user_id)
            # Get all coupons related to this user
            coupons = Coupon.objects.filter(user=user)
            # Serialize the coupon data
            serializer = CouponSerializer(coupons, many=True)
            return Response({'user': user.name, 'coupons': serializer.data}, status=200)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=404)
        


class AddCouponToUserView(APIView):
    def post(self, request):
        # Get the phone number and coupon data from the request
        phone = request.data.get('phone')
        coupon_data = request.data
        adminid = request.data.get('adminid')

        # Ensure admin_phone is provided
        if not adminid:
            return Response({'message': 'Admin ID is required'}, status=400)

        # Check if the requesting user is an admin
        try:
            admin_user = User.objects.get(userid=adminid)
            if not admin_user.admin:
                return Response({'message': 'Only admins can add coupons'}, status=403)
        except User.DoesNotExist:
            return Response({'message': 'Admin user not found'}, status=404)

        # Ensure phone is provided
        if not phone:
            return Response({'message': 'User phone number is required'}, status=400)

        # Ensure coupon fields are provided
        required_fields = ['coupon_code', 'discount_percentage', 'description', 'valid_from', 'valid_to']
        missing_fields = [field for field in required_fields if field not in coupon_data]
        
        if missing_fields:
            return Response({'message': f'Missing fields: {", ".join(missing_fields)}'}, status=400)

        try:
            # Find the user by phone number
            user = User.objects.get(phone=phone)

            # Check if a coupon with the same coupon_code already exists
            if Coupon.objects.filter(coupon_code=coupon_data['coupon_code']).exists():
                return Response({'message': 'Coupon code already exists'}, status=400)

            # Create a new coupon and associate it with the user
            coupon = Coupon(
                coupon_code=coupon_data['coupon_code'],
                discount_percentage=coupon_data['discount_percentage'],
                description=coupon_data['description'],
                minammount=coupon_data['minammount'],  # minaount should be from model typoo and the [minammount] is the api keyword in postman
                valid_from=coupon_data['valid_from'],
                valid_to=coupon_data['valid_to'],
                active=coupon_data.get('active', True),  # default to True if not provided
                user=user
            )
            coupon.save()

            return Response({'message': 'Coupon added successfully', 'coupon_id': coupon.id}, status=201)

        except User.DoesNotExist:
            return Response({'message': 'User with the given phone number does not exist'}, status=404)

        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=500)



class UseCouponView(APIView):
    def post(self, request):
        # Get the coupon code and admin phone number from the request
        coupon_code = request.data.get('coupon_code')
        adminid = request.data.get('adminid')
        amount = request.data.get('amount')

        if not adminid:
            return Response({'message': 'Admin ID is required'}, status=400)

        # Check if the requesting user is an admin
        try:
            admin_user = User.objects.get(userid=adminid)
            if not admin_user.admin:
                return Response({'message': 'Only admins can use coupons'}, status=403)
        except User.DoesNotExist:
            return Response({'message': 'Admin user not found'}, status=404)

        if not coupon_code:
            return Response({'message': 'Coupon code is required'}, status=400)
        if not amount:
            return Response({'message': 'Please enter an amount'}, status=400)

        # Retrieve the coupon once and store it in a variable
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
        except Coupon.DoesNotExist:
            return Response({'message': 'Coupon with the given code does not exist.'}, status=404)

        # Check if the amount is less than the minimum amount required
        if float(amount) < float(coupon.minammount):
            return Response(
                {'message': f"To use this coupon, a minimum amount of {coupon.minammount} is required."},
                status=400
            )

        # Check if the coupon is still active
        if coupon.active:
            # Mark the coupon as used by setting `active` to False
            coupon.active = False
            coupon.save()
            return Response({'message': 'Coupon has been used successfully.' , 'percentage':coupon.discount_percentage}, status=200)
        else:
            return Response({'message': 'Coupon has already been used or expired.'}, status=400)
