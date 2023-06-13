from django.shortcuts import render, HttpResponseRedirect, reverse

from .models import Flight, Passenger

# Create your views here.
def index(request):
    flights = Flight.objects.all()
    return render(request, "flights/index.html", {
        "flights": flights,
    })
    

def flights(request, id):
    flight = Flight.objects.get(pk=id)
    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight)
    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": passengers,
        "non_passengers": non_passengers,
    })
    

def book(request, id):
    if request.method == "POST":
        flight = Flight.objects.get(pk=id)
        passenger_id = int(request.POST["passenger"])
        passenger = Passenger.objects.get(pk=passenger_id)
        passenger.flights.add(flight)
        return HttpResponseRedirect(reverse("flights", args=(flight.id, )))