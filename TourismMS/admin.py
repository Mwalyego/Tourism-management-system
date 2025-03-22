from django.contrib import admin
from django.core.mail import send_mail

# Register your models here.

from .models import Category, Attraction, Tourist, Destination, Booking

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "attraction", "status", "booking_date")
    actions = ["approve_bookings", "cancel_bookings"]

    def approve_bookings(self, request, queryset):
        queryset.update(status="approved")
        for booking in queryset:
            send_mail(
                "Booking Approved",
                f"Dear {booking.user.username},\n\nYour booking for {booking.attraction.name} has been approved!",
                "augustinonyustas@gmail.com",
                [booking.user.email],
                fail_silently=True,
            )
    approve_bookings.short_description = "Approve selected bookings and notify users"

    def cancel_bookings(self, request, queryset):
        queryset.update(status="cancelled")
    cancel_bookings.short_description = "Cancel selected bookings"

@admin.register(Tourist)
class TouristAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'profile_picture')  

    def get_username(self, obj):
        return obj.user.username  #Access username via 'user'
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email  #Access email via 'user'
    get_email.short_description = 'Email'


# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display = ('booking', 'qr_code')

@admin.register(Destination)
class Destination(admin.ModelAdmin):
    list_display = ('name',)

# @admin.register(Service)
# class ServiceAdmin(admin.ModelAdmin):
#     list_display = ('name', 'description', 'provider')
    
# This code registers the
#  models with the Django admin site. The admin.site.
# register() function is used to register the models, 
# along with custom admin classes that define how the
#  models are displayed in the admin interface. 
# The custom admin classes inherit 
# from admin.ModelAdmin and define the list_display
#  attribute to specify which fields are displayed 
# in the list view of the admin interface. T
# his allows administrators to view and m
# anage the data stored in the models through 
# the Django admin site.
