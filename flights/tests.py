from django.test import Client, TestCase
from django.db.models import Max
from .models import Flight, Airport, People, Passenger
from .views import flights
# Create your tests here.

class FlightTestCase(TestCase):
    def setUp(self):
        
        a1 = Airport.objects.create(Code="AAA", City="City A")
        a2 = Airport.objects.create(Code="BBB", City="City B")
        
        Flight.objects.create(Origin=a1, Destination=a2, Duration=100)
        Flight.objects.create(Origin=a2, Destination=a2, Duration=200)
        Flight.objects.create(Origin=a2, Destination=a1, Duration=50)
        Flight.objects.create(Origin=a1, Destination=a2, Duration=-100)
        
    def test_departures_count(self):
        a = Airport.objects.get(Code="AAA")
        self.assertEqual(a.departures.count(), 2)
        
    def test_arrivals_count(self):
        a = Airport.objects.get(Code="BBB")
        self.assertEqual(a.arrivals.count(), 3)
        
    def test_invalid_flight_destination(self):
        a2 = Airport.objects.get(Code="BBB")
        f = Flight.objects.get(Origin=a2, Destination=a2)
        self.assertFalse(f.is_valid_flight())
        
    def test_valid_flight(self):
        a1 = Airport.objects.get(Code="AAA")
        a2 = Airport.objects.get(Code="BBB")
        f = Flight.objects.get(Origin=a1, Destination=a2, Duration=100)
        self.assertTrue(f.is_valid_flight())
        
    def test_invalid_flight_duration(self):
        a1 = Airport.objects.get(Code="AAA")
        a2 = Airport.objects.get(Code="BBB")
        f = Flight.objects.get(Origin=a1, Destination=a2, Duration=-100)
        self.assertFalse(f.is_valid_flight())
        
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 4)
        
        
    def test_valid_flight_page(self):
        a2 = Airport.objects.get(Code="BBB")
        
        f = Flight.objects.get(Origin=a2, Destination=a2)

        c = Client()
        
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"] + 1
        all_id = Flight.objects.all()
        c = Client()
        
        self.assertTrue(max_id not in all_id)
        
    def test_flight_page_passengers(self):
        a2 = Airport.objects.get(Code="BBB")
        
        f = Flight.objects.get(Origin=a2, Destination=a2)
        
        pe = People.objects.create(first_name="Alice", last_name="Adams")
        
        p = Passenger.objects.create(people_id=pe.id)
        f.passengers.add(p)

        c = Client()
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self):
        a1 = Airport.objects.get(Code="AAA")
        a2 = Airport.objects.get(Code="BBB")
        
        f = Flight.objects.get(Origin=a2, Destination=a1)
        
        pe = People.objects.create(first_name="Alice", last_name="Adams")
        
        p = Passenger.objects.create(people_id=pe.id)
                
        c = Client()
        
        response = c.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)



    
    
    
    
    
    