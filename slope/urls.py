from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("reset", views.reset, name="reset"),
    path("pdf/<str:max_fos>", views.pdf, name="pdf"),
]
