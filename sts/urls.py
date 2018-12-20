from django.urls import path

from . import views


urlpatterns = [
    path('', views.hello, name='hello'),
    path('dp', views.do_push, name='do_push'),
    path('es', views.edit_staff, name='edit_staff'),
    path('np', views.new_projs, name='new_projs'),

    path('c', views.create, name='create'),
]
