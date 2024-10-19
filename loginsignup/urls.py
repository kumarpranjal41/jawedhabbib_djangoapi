from django.urls import path, include
from rest_framework.routers import DefaultRouter
from loginsignup.views import UserViewSet, LoginViewSet, UserCouponsView , AddCouponToUserView , UseCouponView

router = DefaultRouter()
router.register(r'signup', UserViewSet)
# router.register(r'coupons', CouponViewSet)  # Register the Coupon route

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('user/<int:user_id>/coupons/', UserCouponsView.as_view(), name='user-coupons'),
    path('add-coupon/', AddCouponToUserView.as_view(), name='add-coupon'),
    path('use-coupon/', UseCouponView.as_view(), name='use_coupon'),

]
