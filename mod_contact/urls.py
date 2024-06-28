from django.urls import path
from mod_contact import views

# Gestion des routes
urlpatterns = [
    path('get_contact_filter/', views.get_contact_filter, name='get_contact_filter'),
    path('create_contact/', views.create_contact, name='create_contact'),
    path('update_contact/<int:pk>', views.update_contact, name='update_contact'),
    path('delete_contact/<int:pk>', views.delete_contact, name='delete_contact'),
]