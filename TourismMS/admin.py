from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Category, Attraction, Tourist, Booking, Ticket, Service, ContentCreator

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location')

@admin.register(Tourist)
class TouristAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profile_picture')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('tourist', 'attraction', 'booking_date', 'booking_number', 'payment_status')

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('booking', 'qr_code')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'provider')

@admin.register(ContentCreator)
class ContentCreatorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

