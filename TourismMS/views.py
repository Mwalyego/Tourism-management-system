from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render,redirect
from .models import Booking, Destination,Attraction
from django.http import HttpResponse, JsonResponse
from django.utils import timezone  # Import timezone
from django.template.loader import render_to_string
import pdfkit
from django.db.models import Count

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin')  # Admin dashboard
        else:
            return redirect('/normDashboard')  # Normal user dashboard
    return render(request, 'index.html')  # Show index only if not logged in

def contact(request):
    return render(request, "contact.html")

def services(request):
    return render(request,"services.html")

def about(request):
    return render(request,"about.html")

def destination(request):
    return render(request,"destination.html")

def normDashboard(request):
    # Get the most popular destinations based on bookings
    popular_destinations = Destination.objects.annotate(
        booking_count=Count('attractions__booking')
    ).order_by('-booking_count')[:5]  # Limit to top 5 destinations

    # Add an image from one of the attractions for each destination
    destinations_with_images = []
    for destination in popular_destinations:
        attraction = destination.attractions.first()  # Get the first attraction for the destination
        if attraction and attraction.image:  # Ensure the attraction has an image
            destinations_with_images.append({
                'name': destination.name,
                'image': attraction.image.url,
                'booking_count': destination.booking_count
            })

    return render(request, 'normDashboard.html', {'popular_destinations': destinations_with_images})

def get_attractions_by_destination(request):
    destination_id = request.GET.get("destination_id")

    if destination_id and destination_id != "all":
        attractions = Attraction.objects.filter(destination_id=destination_id)
    else:
        attractions = Attraction.objects.all()  # Get all attractions

    data = [
        {
            "id": attraction.id,
            "name": attraction.name,
            "description": attraction.description,
            "location": attraction.location,
            "price": attraction.price,
            "image": request.build_absolute_uri(attraction.image.url) if attraction.image else None
        }
        for attraction in attractions
    ]

    # Fetch all destinations dynamically
    destinations = list(Destination.objects.values("id", "name"))

    return JsonResponse({
        "attractions": data,
        "destinations": destinations  #returning destinations
    })

def book_attraction(request, attraction_id):
    attraction = get_object_or_404(Attraction, id=attraction_id)

    if request.method == "POST":
        booking = Booking.objects.create(
            user=request.user,
            attraction=attraction,
            status="pending",  # Default status is pending
            booking_date=timezone.now()  # Set the current date and time
        )
        return redirect("payment-info")  # Redirect to payment info page

    return render(request, "booking.html", {"attraction": attraction})

def payment_info(request):
    return render(request, "payment_info.html")

def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'profile.html', {'bookings': bookings})

def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != "approved":
        return HttpResponse("Payment not approved yet.", status=403)

    html = render_to_string("ticket.html", {"booking": booking})
    pdf = pdfkit.from_string(html, False)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=ticket_{booking.id}.pdf"

    return response
