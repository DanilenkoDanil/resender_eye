from api.views import GetInfoApiView
from django.urls import path, include

urlpatterns = [
    path('get-info/', GetInfoApiView.as_view(), name='get-info/'),
]