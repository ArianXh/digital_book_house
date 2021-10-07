"""digital_book_house URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls import include
from django.urls import path

from django.contrib.auth.views import LoginView,LogoutView

from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.home_view),

    path('admin', views.adminclick_view),
    path('adminsignup', views.adminsignup_view),
    path('adminlogin', LoginView.as_view(template_name='library/adminlogin.html')),

    path('user', views.userclick_view),
    path('usersignup', views.usersignup_view),
    path('userlogin', LoginView.as_view(template_name='library/userlogin.html')),

    path('logout', LogoutView.as_view(template_name='library/index.html')),
    path('afterlogin', views.afterlogin_view),

    path('addbook', views.addkniga_view),
    path('viewbook', views.viewkniga_view),
    path('book/<int:pk>', views.KnigaDetailView.as_view(), name='book-detail'),


    path('issuebook', views.add_pozajmica_kniga_view),
    path('viewissuedbook', views.pozajmica_kniga_view),
    #path('viewissuedbookbyuser', views.viewissuedbookbyuser),

    path('viewuser', views.viewuser_view),
    path('clen/<int:pk>', views.LugjeDetailView.as_view(), name='clen-detail'),



    path('aboutus', views.aboutus_view),

    path('contactus', views.contactus_view),

]
