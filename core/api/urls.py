from django.urls import path
from .views import (
    RegistrationAPIView, VerifyOTPAPIView, 
    LogoutBlacklistTokenUpdateView, MyTokenObtainPairView, 
    UsersAPIView, UserDetailAPIView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [

    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('verify/', VerifyOTPAPIView.as_view(), name='verify-otp'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutBlacklistTokenUpdateView.as_view(), name='logout'),
    path('register/', RegistrationAPIView.as_view(), name='registration'),
    path('users/', UsersAPIView.as_view(), name='users-list'),
    path('users/<int:id>/', UserDetailAPIView.as_view(), name='users-detail')
    # path('experiment/', DemoView.as_view(),name='demo'),
    # path('experiment2/', DemoView2.as_view(),name='demo2')

]