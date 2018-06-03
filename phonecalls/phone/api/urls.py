from django.urls import path

from phone.api.views import PhoneCallAdd

app_name = 'phone'

urlpatterns = [
    path('call/', PhoneCallAdd.as_view(),
         name="call_add"),
]
