"""molimoli URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
# import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home_page.urls', namespace='home_page')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('forum/', include('forum.urls', namespace='forums')),
]


handler404 = "home_page.views.page_not_found"

handler500 = "home_page.views.page_error"
