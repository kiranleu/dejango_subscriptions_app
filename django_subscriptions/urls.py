"""djangosubs URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from accounts.views import home, signup, profile
from billing.views import add_credit_card, remove_credit_card, make_payment, subscribe, unsubscribe
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', signup, name='signup'),
    path('accounts/profile/', profile, name='profile'),
    path('billing/add_credit_card/', add_credit_card, name='add_credit_card'),
    path('billing/remove_credit_card/', remove_credit_card, name='remove_credit_card'),
    path('billing/make_payment/', make_payment, name='make_payment'),
    path('billing/subscribe/', subscribe, name='subscribe'),
    path('billing/unsubscribe/', unsubscribe, name='unsubscribe'),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]