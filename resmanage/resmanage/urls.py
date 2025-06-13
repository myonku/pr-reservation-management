"""
URL configuration for resmanage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from api.views import login_Action, adminin, login_Action, registerAction, register, logins, error_page   #已弃用

urlpatterns = [
    path(route="", view=login_Action),
    path(route="admin/", view=adminin, name="admin"),
    path(route="admins/", view=admin.site.urls),  # 管理后台
    path(route="loginAction/", view=login_Action, name="loginAction"),
    path(route="login/", view=logins, name="login"),
    path(route="registerAction/", view=registerAction, name="registerAction"),
    path(route="register/", view=register, name="register"),
    # error
    path(route="error/", view=error_page, name="error"),
    # 分发路由:
    #path(route="homepage/", view=include("api.urls")),
    #path(route="verif/", view=include("api.urls1")),
    #path(route="manage/", view=include("api.urls2")),
    # 以上除管理后台均已弃用
    # 数据接口路由:
    path(route="api/", view=include("resvation.urls")),
    #
] + static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
