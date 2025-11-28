from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render, redirect
from .models import Booking, Destination, Attraction
from django.http import HttpResponse, JsonResponse
from django.utils import timezone  # Import timezone
from django.template.loader import render_to_string
import pdfkit
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect("/admin")  # Admin dashboard
        else:
            return redirect("/normDashboard")  # Normal user dashboard

    # Fetch all destinations and their attractions
    destinations = Destination.objects.all()

    # Handle search query (GET param `q`)
    q = request.GET.get("q", "").strip()
    search_query = q if q else None
    search_results = []

    if search_query:
        matches = (
            Attraction.objects.select_related("destination")
            .filter(
                Q(name__icontains=search_query)
                | Q(description__icontains=search_query)
                | Q(location__icontains=search_query)
                | Q(destination__name__icontains=search_query)
            )
            .distinct()
        )

        for attr in matches:
            search_results.append(
                {
                    "id": attr.id,
                    "name": attr.name,
                    "description": attr.description,
                    "location": attr.location,
                    "price": attr.price,
                    "image": attr.image.url if getattr(attr, "image", None) else None,
                    "destination_name": (
                        attr.destination.name
                        if getattr(attr, "destination", None)
                        else ""
                    ),
                }
            )

    # Build a data structure: each destination with its attractions
    destination_data = []
    for dest in destinations:
        attractions = dest.attractions.all()
        destination_data.append(
            {
                "id": dest.id,
                "name": dest.name,
                "attractions": [
                    {
                        "id": attr.id,
                        "name": attr.name,
                        "description": attr.description,
                        "location": attr.location,
                        "price": attr.price,
                        "image": (
                            attr.image.url if getattr(attr, "image", None) else None
                        ),
                    }
                    for attr in attractions
                ],
            }
        )

    context = {
        "destinations": destinations,
        "destination_data": destination_data,
        "search_query": search_query,
        "search_results": search_results,
    }

    return render(request, "index.html", context)  # Show index only if not logged in


def contact(request):
    return render(request, "contact.html")


def services(request):
    return render(request, "services.html")


def about(request):
    return render(request, "about.html")


@login_required(login_url="login")
def destination(request):
    return render(request, "destination.html")


@login_required(login_url="login")
def normDashboard(request):
    # 1) Popular destinations based on bookings (top 6)
    popular_qs = Destination.objects.annotate(
        booking_count=Count("attractions__booking")
    ).order_by("-booking_count")[:6]

    popular_destinations = []
    for dest in popular_qs:
        attraction = dest.attractions.first()
        img = (
            attraction.image.url
            if (attraction and getattr(attraction, "image", None))
            else None
        )
        popular_destinations.append(
            {
                "id": dest.id,
                "name": dest.name,
                "image": img,
                "booking_count": getattr(dest, "booking_count", 0),
            }
        )

    # 2) Destination with the most attractions
    dest_most_attractions = (
        Destination.objects.annotate(attraction_count=Count("attractions"))
        .order_by("-attraction_count")
        .first()
    )

    destination_most_attractions = None
    if dest_most_attractions:
        attr = dest_most_attractions.attractions.first()
        destination_most_attractions = {
            "id": dest_most_attractions.id,
            "name": dest_most_attractions.name,
            "attraction_count": getattr(dest_most_attractions, "attraction_count", 0),
            "image": (
                attr.image.url if (attr and getattr(attr, "image", None)) else None
            ),
        }

    # 3) Recent popular destinations (by recent bookings)
    recent_destinations = []
    seen = set()
    bookings = Booking.objects.select_related("attraction__destination").order_by(
        "-booking_date"
    )
    for b in bookings:
        dest = b.attraction.destination
        if dest.id in seen:
            continue
        seen.add(dest.id)
        attr = dest.attractions.first()
        # Format booking datetime to a human-readable string to avoid template date-filter errors
        try:
            last_booked_str = timezone.localtime(b.booking_date).strftime(
                "%b %d, %Y %H:%M"
            )
        except Exception:
            # Fallback to string conversion if something goes wrong
            last_booked_str = str(b.booking_date)

        recent_destinations.append(
            {
                "id": dest.id,
                "name": dest.name,
                "image": (
                    attr.image.url if (attr and getattr(attr, "image", None)) else None
                ),
                "last_booked": last_booked_str,
            }
        )
        if len(recent_destinations) >= 6:
            break

    context = {
        "popular_destinations": popular_destinations,
        "destination_most_attractions": destination_most_attractions,
        "recent_popular_destinations": recent_destinations,
    }

    return render(request, "normDashboard.html", context)


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
            "image": (
                request.build_absolute_uri(attraction.image.url)
                if attraction.image
                else None
            ),
        }
        for attraction in attractions
    ]

    # Fetch all destinations dynamically
    destinations = list(Destination.objects.values("id", "name"))

    return JsonResponse(
        {"attractions": data, "destinations": destinations}  # returning destinations
    )


@login_required(login_url="login")
def book_attraction(request, attraction_id):
    attraction = get_object_or_404(Attraction, id=attraction_id)

    if request.method == "POST":
        booking = Booking.objects.create(
            user=request.user,
            attraction=attraction,
            status="pending",  # Default status is pending
            booking_date=timezone.now(),  # Set the current date and time
        )
        return redirect("payment-info")  # Redirect to payment info page

    return render(request, "booking.html", {"attraction": attraction})


@login_required(login_url="login")
def payment_info(request):
    return render(request, "payment_info.html")


@login_required(login_url="login")
def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by("-booking_date")
    return render(request, "profile.html", {"bookings": bookings})


@login_required(login_url="login")
def download_ticket(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != "approved":
        return HttpResponse("Payment not approved yet.", status=403)

    html = render_to_string("ticket.html", {"booking": booking})
    pdf = pdfkit.from_string(html, False)

    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=ticket_{booking.id}.pdf"

    return response
