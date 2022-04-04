from api.views import GetInfoApiView, GetAuthCode, InputCode
from django.urls import path, include

urlpatterns = [
    path('get-info/', GetInfoApiView.as_view(), name='get-info/'),
    path('get-code/', GetAuthCode.as_view(), name='get-code/'),
    path('input-code/', InputCode.as_view(), name='input-code/'),
]