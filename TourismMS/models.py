from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
import pdfkit
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Destination(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Attraction(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    destination=models.ForeignKey(Destination,on_delete=models.CASCADE,related_name='attractions')
    location = models.CharField(max_length=255)
    price=models.IntegerField()
    image = models.ImageField(upload_to='attractions/')

    def __str__(self):
        return self.name
    
class Tourist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)


class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending Payment"),
        ("approved", "Approved"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attraction = models.ForeignKey("Attraction", on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)  # Ensure default value is set
    booking_number = models.CharField(max_length=12, unique=True, editable=False)
    status = models.CharField(max_length=20, default="pending")

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = str(uuid.uuid4().hex[:12].upper())  # Generate a unique booking number
        if not self.booking_date:
            self.booking_date = timezone.now()  # Explicitly set booking_date if not provided
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.attraction.name} ({self.booking_date}) - {self.status}"
    
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != "approved":
        return HttpResponse("Payment not approved yet.", status=403)

    html = render_to_string("ticket_template.html", {"booking": booking})
    pdf = pdfkit.from_string(html, False)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=ticket_{booking.id}.pdf"

    return response






