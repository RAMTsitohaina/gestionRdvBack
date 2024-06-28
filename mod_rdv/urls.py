from django.urls import path
from mod_rdv import views

# Gestions des routes
urlpatterns = [
    path('get_rdv_filter/', views.get_rdv_filter, name='get_rdv_filter'),
    path('create_rdv/', views.create_rdv, name='create_rdv'),
    path('update_rdv/<int:pk>', views.update_rdv, name='update_rdv'),
    path('delete_rdv/<int:pk>', views.delete_rdv, name='delete_rdv'),
]