from django.urls import path, include
from .views import RegisterView, LoginView, OTPVerifyView, OTPRefreshView, SendMailToResetPasswordView, ResetPasswordView, MyAccountInfoView, SecurityView

urlpatterns = [
    path('account/', include([
      path('register', RegisterView.as_view(), name='register'),
      path('login', LoginView.as_view(), name='login'),
      path('reset/', include([
        path('send-mail', SendMailToResetPasswordView.as_view(), name='send-mail'),
        path('tk/<str:ticket>', ResetPasswordView.as_view(), name='reset-passowrd')
      ])),
      path('otp/', include([
        path('verify', OTPVerifyView.as_view(), name='verify'),
        path('refresh', OTPRefreshView.as_view(), name='refresh')
      ])),
      path('profile', MyAccountInfoView.as_view(), name='profile'),
      path('security', SecurityView.as_view(), name='security')
    ])),
]
