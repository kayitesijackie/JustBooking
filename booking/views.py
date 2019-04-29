from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import BusOrganisation, Route, Bus, Schedule, Ticket
from datetime import datetime, date
from django.contrib.auth.decorators import login_required

from .forms import TicketForm, ScheduleForm
import uuid
# import phonenumbers
# from AfricasTalkingGateway import AfricasTalkingGateway, AfricasTalkingGatewayException
# from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
# from decouple import config
# from django.utils import urlencode

def home(request):
    '''
    view function for landing page
    '''
    return render(request, 'home.html')

def search_results(request):
    '''
    View function to get the the requested departure and arrival locations from the database and display to the user
    '''
    try:
        title = 'Result'

        if ('depature-location' in request.GET and request.GET['depature-location']) and ('arrival-location' in request.GET and request.GET['arrival-location']) and ('travel-date' in request.GET and request.GET['travel-date']):

            # Get the input departure
            search_departure_location = request.GET.get('depature-location').title()

            # Get the input arrival location
            search_arrival_location = request.GET.get('arrival-location').title()

            # Get the input date
            travel_date = request.GET.get('travel-date')

            # Convert string input to date type
            convert_to_date = datetime.strptime(travel_date, '%Y-%m-%d').date()

            # Get the route 
            result_route = Route.get_search_route(search_departure_location,search_arrival_location)
            print(result_route)

            # Check if route exists found
            if result_route != None :
                
                # Schedule with the same depature date
                schedule_with_depature_date = Schedule.get_departure_buses(convert_to_date, result_route.id)

                if len(schedule_with_depature_date) > 0:

                    for schedule in schedule_with_depature_date:

                        estimation_duration = Schedule.get_travel_estimation(schedule.id)

                    return render(request, 'search.html', {'title':title, 'search_departure_location':search_departure_location, 'search_arrival_location':search_arrival_location, 'convert_to_date':convert_to_date, 'buses':schedule_with_depature_date, 'estimation_duration':estimation_duration})

                else:
                    print('no scheduled buses')
                    no_scheduled_bus_message = 'No scheduled buses'

                    return render(request, 'search.html', {'title':title, 'no_scheduled_bus_message':no_scheduled_bus_message, 'search_departure_location':search_departure_location, 'search_arrival_location':search_arrival_location, 'convert_to_date':convert_to_date})

            # Otherwise
            else:
                
                no_route_message = 'Bus route not found'

                return render(request, 'search.html', {'title':title, 'no_route_message':no_route_message, 'search_departure_location':search_departure_location, 'search_arrival_location':search_arrival_location, 'convert_to_date':convert_to_date})
        
    except ObjectDoesNotExist:

        return redirect(Http404)

def bus_details(request, bus_schedule_id):
    '''
    View function to display a form for the user to fill to get a ticket
    '''
    try:
        # args = {}

        selected_bus = Schedule.get_single_schedule(bus_schedule_id)

        # title = f'{selected_bus.bus.bus_organisation} 

        estimation_duration = Schedule.get_travel_estimation(bus_schedule_id)

        if request.method == 'POST':
            
            form = TicketForm(request.POST)

            if form.is_valid():
                
                ticket = form.save(commit=False)

                ticket.schedule = selected_bus

                ticket.ticket_number = uuid.uuid4()

                ticket.save()

                ticket_id = ticket.id

                return redirect(mobile_payment, ticket_id)

        else:

            form = TicketForm()

        # args['form'] = form

        return render(request, 'bus_details.html', {'title':title, 'form':form, 'selected_bus':selected_bus, 'estimation_duration':estimation_duration})

    except ObjectDoesNotExist:

         return redirect(Http404)


@login_required(login_url='/accounts/login/')
def submit_schedule(request):
    current_user = request.user
    if request.method == 'POST':
        form =ScheduleForm(request.POST)

        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = current_user
            schedule.save()
            return redirect(reverse('schedule'))
    else:
        form = ScheduleForm()

    return render(request,'schedule_form.html',{'form':form})

def schedule(request):
    schedules = Schedule.objects.all()
    return render(request,'schedule.html',{'schedules':schedules})







