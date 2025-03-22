from django.urls import path

from . import views
from .views import get_attractions_by_destination,payment_info    
urlpatterns = [
    path('', views.index, name='index'),
    path('contact/', views.contact, name='contact'),
    path('services/',views.services,name='services'),
    path('about/',views.about,name='about'),
    path('destination/',views.destination,name='destination'),
    path('normDashboard/',views.normDashboard,name='normDashboard'),
    path("get-attractions/", get_attractions_by_destination, name="get_attractions"),
    path("book-attraction/<int:attraction_id>/", views.book_attraction, name="book_attraction"),
    path("payment-info/", payment_info, name="payment-info"),
    path("profile/", views.profile, name="profile"),
    path('download-ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),

]       