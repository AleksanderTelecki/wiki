from django.urls import path

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/newpage",views.newPage,name="newPage"),
    path("wiki/editpage/<str:entryName>",views.editPage,name="editPage"),
    path("wiki/randompage",views.RandomPage,name="RandomPage"),
    path("wiki/<str:entryName>",views.showEntry,name="showEntry")
    
]
