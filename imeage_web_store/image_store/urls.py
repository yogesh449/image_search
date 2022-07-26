from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('search/', views.get_images, name='image_search'),
    path('images_pdf/', views.images_to_pdf, name='image_pdf'),
]

urlpatterns += staticfiles_urlpatterns()