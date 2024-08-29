from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Attraction(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='attractions/')

    def __str__(self):
        return self.name

class Tourist(User):
    # Inherits from Django's built-in User model
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # Add any additional fields here

class Booking(models.Model):
    tourist = models.ForeignKey(Tourist, on_delete=models.CASCADE)
    attraction = models.ForeignKey(Attraction, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_number = models.CharField(max_length=100, unique=True)
    payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Pending', 'Pending')])

    def save(self, *args, **kwargs):
        if not self.booking_number:
            self.booking_number = self.generate_booking_number()
        super().save(*args, **kwargs)

    def generate_booking_number(self):
        # Generate a unique booking number
        return f'BOOK-{self.pk}'

    def __str__(self):
        return f'Booking {self.booking_number} by {self.tourist.username}'

class Ticket(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to='tickets/')

    def save(self, *args, **kwargs):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(self.booking.booking_number)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        qr_io = BytesIO()
        img.save(qr_io, format='PNG')
        qr_file = ContentFile(qr_io.getvalue(), 'qr_code.png')
        self.qr_code.save('qr_code.png', qr_file, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Ticket for Booking {self.booking.booking_number}'

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    provider = models.ForeignKey(Tourist, on_delete=models.CASCADE)  # Assuming provider is a Tourist for simplicity

    def __str__(self):
        return self.name

class ContentCreator(models.Model):
    user = models.OneToOneField(Tourist, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username

