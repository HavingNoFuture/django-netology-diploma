"""shop URL Configuration

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
from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView

from app.views import account_view, registration_view, login_view

urlpatterns = [
    path('', RedirectView.as_view(url=reverse_lazy('main_page'))),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('account/', account_view, name='account'),
    path('account/login/', login_view, name='login'),
    path('account/registration/', registration_view, name='registration'),
    path('account/logout/', LogoutView.as_view(next_page=reverse_lazy('main_page')), name='logout'),
    path('shop/', include('app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, documenmt_root=settings.STATIC_ROOT)
