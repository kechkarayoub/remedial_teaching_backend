"""remedial_teaching URL Configuration

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
from home import views
from django.contrib import admin
from django.urls import include, path, re_path
#from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('feeds_languages_api', views.feeds_languages_api, name='feeds_languages_api'),
    path('general_information_api', views.general_information_api, name='general_information_api'),
    path('services_accounts_types_api', views.services_accounts_types_api, name='services_accounts_types_api'),
    path('user/', include('user.urls')),
    path('utils/', include('utils.urls')),
]
urlpatterns += i18n_patterns(
    re_path(r'^admin/', admin.site.urls),
    prefix_default_language=True
)
