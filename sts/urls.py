from django.urls import path

from . import views


urlpatterns = [
    path('', views.hello, name='hello'),
    path('p', views.push_, name='push'),
    path('es', views.edit_staff, name='edit_staff'),
    path('np', views.new_projs, name='new_projs'),

    path('login', views.login, name='login'),

    path('c', views.create, name='create')
]
