from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('about/', views.about, name="about"),
    path('logout/', views.logoutpage, name="logout"),

    path('add-brand/', views.add_brand, name="add-brand")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)