from django.urls import re_path

from bill.api.views import BillDetailList

app_name = 'bill'

urlpatterns = [
    re_path(r'(?P<source_number>[0-9]+)/', BillDetailList.as_view(),
            name="bill_detail_list"),
]
