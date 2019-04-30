from django.db import models
from datetime import datetime, date, time, timedelta
from django.utils import timezone
import datetime as dt
import uuid
from decimal import Decimal

# Create your models here.
class BusOrganisation(models.Model):
    
    name = models.CharField(max_length=255)

    logo = models.ImageField(upload_to="logo-pic/", blank=True) 

    def __str__(self):
        return self.name

    @classmethod
    def get_bus_organisations(cls):
       
        bus_organisations = cls.objects.all()

        return bus_organisations

    @classmethod
    def get_single_bus_organisation(cls, bus_organisation_id):
        
        single_bus_origanisation = cls.objects.get(id=bus_organisation_id)

        return single_bus_origanisation

class Route(models.Model):
    
    departure_location = models.CharField(max_length=255)

    destination_location = models.CharField(max_length=255)

    def __str__(self):
        return self.departure_location + '-' + self.destination_location

    @classmethod
    def get_routes(cls):
        
        routes = cls.objects.all()

        return routes

    @classmethod
    def get_single_route(cls, route_id):
        
        single_route = cls.objects.get(id=route_id)

        return single_route

    @classmethod
    def get_search_route(cls, search_departure_location, search_arrival_loaction):
        

        found_routes = cls.objects.filter(departure_location=search_departure_location).filter(destination_location=search_arrival_loaction)

        existing_routes = cls.objects.all()

        # Get each existing route
        for existing_route in existing_routes:

            # Get each found route
            for found_route in found_routes:

                if existing_route == found_route:

                     return found_route

                # Otherwise
                else:

                    continue
        return None

class Bus(models.Model):
    
    bus_organisation = models.ForeignKey(BusOrganisation, on_delete=models.CASCADE)

    number_plate = models.CharField(max_length=50)

    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    seats = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.bus_organisation.name + ' Bus No.' + str(self.id)

    @classmethod
    def get_buses(cls):
        
        buses = cls.objects.all()

        return buses

    @classmethod
    def get_single_bus(cls, bus_id):
        
        single_bus = cls.objects.get(id=bus_id)

        return single_bus

    @classmethod
    def get_bus_organisation_buses(cls, bus_organisation_id):
       
        bus_origanisation_buses = cls.objects.filter(bus_organisation=bus_organisation_id)

        return bus_origanisation_buses

    @classmethod
    def get_route_buses(cls, route_id):
        
        route_buses = cls.objects.filter(route=route_id)

        return route_buses

class Schedule(models.Model):
    departure_location = models.CharField(max_length=255, null= True)

    destination_location = models.CharField(max_length=255, null= True)
    
    departure_time = models.TimeField(default=dt.time(00, 00))

    date = models.DateField(("Date"), default=date.today)

    name= models.ForeignKey(BusOrganisation, on_delete=models.CASCADE, null= True)

    price = models.DecimalField(max_digits=15 ,decimal_places=2, default=Decimal(0.00))

    # def __str__(self):
    #     return self.bus.bus_organisation.name + ' Bus No.' + str(self.bus.id) + ' Schedule No.' + str(self.id)

    class Meta:
       
        ordering = ['price']

    @classmethod
    def get_schedules(cls,name):
        
        schedule = cls.objects.all.filter(name=name)

        return schedule

    @classmethod
    def get_single_schedule(cls, schedule_id):
        
        single_schedule = cls.objects.get(id=schedule_id)

        return single_schedule

    @classmethod
    def get_bus_schedules(cls, bus_id):
        
        bus_schedules = cls.objects.filter(bus=bus_id)

        return bus_schedules

    @classmethod
    def get_travel_estimation(cls, schedule_id):
        
        schedule = cls.objects.get(id=schedule_id)

        calculate_travel_estimation = schedule.arrival_time - schedule.departure_time

        travel_estimation = str(calculate_travel_estimation.seconds//3600) + ' hours ' + str(calculate_travel_estimation.seconds//60 % 60) + ' minutes'

        return travel_estimation

    @classmethod
    def get_departure_buses(cls, departure_date, route_id):
        
        departure_datetime = datetime.combine(departure_date, time(tzinfo=timezone.get_current_timezone()))

        # print(departure_datetime)
        next_date = departure_datetime + timedelta(days=1)
        # print(next_date)

        # Get allschedules in the 24 hour period
        found_buses = cls.objects.filter(departure_time__range=(departure_datetime, next_date))

        # List of buses departing
        departure_buses = []

        for found_bus in found_buses:
            # Check if route id is the same

            if found_bus.bus.route.id == route_id:

                departure_buses.append(found_bus)
                continue

        return departure_buses

class Ticket(models.Model):
    
    first_name = models.CharField(max_length = 255)
    
    last_name = models.CharField(max_length = 255)

    email = models.EmailField(max_length = 254)
    
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length = 255)

    ticket_number = models.UUIDField(default = uuid.uuid4, editable = False)

    transaction_code = models.CharField(max_length = 255)

    def __str__(self):
        
        return self.first_name + ' ' + self.last_name + ' ' + str(self.ticket_number)

    @classmethod
    def get_tickets(cls):
        
        tickets = cls.objects.all()
        
        return tickets

    @classmethod
    def get_single_ticket(cls, ticket_id):
                
        single_ticket = cls.objects.get(id = ticket_id)

        return single_ticket







