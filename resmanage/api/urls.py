"""已弃用"""

from django.urls import path
from api.views import index

urlpatterns = [
    path("index/", index, name="index"),
]


# urls1.py
"""已弃用"""

""" from django.urls import path
from .views import valid_res_list, all_res_list, res_detail, apd_record_list

urlpatterns = [
    path("audit/", valid_res_list, name="audit"),
    path("navi/", all_res_list, name="navi"),
    path("apd_list/", apd_record_list, name="apd_list"),
    path("sodetail/", res_detail, name="sodetail"),
] """

# urls2.py

""" from django.urls import path
from .views import sep_manage, device_manage

urlpatterns = [
    path("smanage/", sep_manage, name="sep_manage"),
    path("dmanage/", device_manage, name="device_manage"),
] """
