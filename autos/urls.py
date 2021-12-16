from django.urls import path

from . import views

app_name = 'autos'

urlpatterns = [
    # # ex: /autos/
    # path('', views.IndexView.as_view(), name='index'),
    path('', views.MainView.as_view(), name='all'),

    #Main - Create Autos
    path('main/create/', views.AutoCreate.as_view(), name='auto_create'),
    #Main - Update Autos
    path('main/<int:pk>/update/', views.AutoUpdate.as_view(), name='auto_update'),
    #Min - Delete Autos
    path('main/<int:pk>/delete/', views.AutoDelete.as_view(), name='auto_delete'),

    #Lookup
    path('lookup/', views.MakeView.as_view(), name='make_list'),

    #Lookup - Create by PK
    path('lookup/create/', views.MakeCreate.as_view(), name='make_create'),
    #Lookup - Edit by PK
    path('lookup/<int:pk>/update/', views.MakeUpdate.as_view(), name='make_update'),
    #Lookup - Delete by PK
    path('lookup/<int:pk>/delete/', views.MakeDelete.as_view(), name='make_delete'),

]