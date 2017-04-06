import os
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from Project.core import views as core_views
from Project.search import views as search_views
from django.contrib import admin
from Project.findRecipe import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'food_picture/$', views.food_picture,
        name='findRecipe'),
]
