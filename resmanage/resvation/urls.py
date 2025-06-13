from django.urls import path
from api.views import (
    #get_weather,  废弃
    get_res_list,
    get_Charts,
    get_error_data,
    get_res_detail,
    get_apd_report,
    username_validator,
)

from api.utils import get_weather

from resvation.views import (  # api接口
    v_register,
    v_login,
    verify_token,
    get_user_info,
    v_apd_report,
    v_res_list,
    get_all_dev,
    get_search_result,
    getchart1,
    getchart2,
    getchart3,
    get_appointments,
    get_user_detail,
    update_qrcode,
    get_all_valid_date,
    get_base_date_info,
    get_date_hours,
    resvation_submit,
    get_frames,
    del_identity,
    get_record_detail,
    asc_record,
    update_appointments,
    get_date_detail,
)


urlpatterns = [
    path("weather", get_weather, name="weather"),  # 公用
    path("vlist", get_res_list, name="get_res_list"),
    path("charts", get_Charts, name="get_Charts"),
    path("error", get_error_data, name="get_error_data"),
    path("res_detail", get_res_detail, name="get_res_detail"),
    path("apd_res_list", get_apd_report, name="get_apd_report"),
    path("username_validator", username_validator, name="username_validator"),  # 公用
    # 以下是为vue端的api接口,存储在resvation.views中
    path("v_login", v_login, name="v_login"),
    path("verify_token", verify_token, name="verify_token"),
    path("v_register", v_register, name="v_register"),
    path("get_user_info", get_user_info, name="get_user_info"),
    path("v_apd_report", v_apd_report, name="v_apd_report"),
    path("v_res_list", v_res_list, name="v_res_list"),
    path("get_all_dev", get_all_dev, name="get_all_dev"),
    path("get_search_result", get_search_result, name="get_search_result"),
    path("charts1", getchart1, name="charts1"),
    path("charts2", getchart2, name="charts2"),
    path("charts3", getchart3, name="charts3"),
    path("get_appointments", get_appointments, name="get_appointments"),
    path("get_user_detail", get_user_detail, name="get_user_detail"),
    path("update_qrcode", update_qrcode, name="update_qrcode"),
    path("get_all_valid_date", get_all_valid_date, name="get_all_valid_date"),
    path("get_base_date_info", get_base_date_info, name="get_base_date_info"),
    path("get_date_hours", get_date_hours, name="get_date_hours"),
    path("resvation_submit", resvation_submit, name="resvation_submit"),
    path("get_frames", get_frames, name="get_frames"),
    path("del_identity", del_identity, name="del_identity"),
    path("get_record_detail", get_record_detail, name="get_record_detail"),
    path("asc_record", asc_record, name="asc_record"),
    path("update_appointments", update_appointments, name="update_appointments"),
    path("get_date_detail", get_date_detail, name="get_date_detail"),
]
