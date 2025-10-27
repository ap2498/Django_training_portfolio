"""
URL configuration for portfolio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.entry,name="load_entry"),
    path('view_index/',views.load_home_page,name='index'),
    path('load_create_projects/',views.load_create_project,name='load_create_projects'),
    path('create_project/',views.create_project,name='create_project'),
    path('create_category/',views.create_category,name='create_category'),
    path('view_all_projects/',views.fetch_all_projects,name='fetch_all_projects'),
    path('single_project/',views.load_single_project_page,name='single_project'),
    path('view_one_project/<int:pk>/',views.fetch_single_project,name='fetch_one_project'),
    path('fetch_by_category/<int:id>/',views.fetch_by_category,name='fetch_by_category'),
    path('get_categories/',views.get_categories,name='get_categories'),
    path('logout_custom/',views.logout_user,name='logout_custom'),
    path('login_custom/',views.login_user,name='login_custom'),
    path('signup/',views.signup,name='signup'),
    path('load_login/',views.load_login,name='load_login'),



]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
