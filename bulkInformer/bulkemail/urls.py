from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("upload",views.file_upload_view,name="file_upload_view")
    
]

