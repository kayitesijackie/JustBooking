from django import forms
# from django.contrib.auth.forms import AuthenticationForm
from .models import *
# import phonenumbers
import datetime as dt
HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

class TicketForm(forms.ModelForm):
  '''
  Class to create a form for a user to get a ticket
  '''

  class Meta:
    model = Ticket

    fields = ('first_name', 'last_name', 'email', 'phone_number')

  def clean(self):
    
    cleaned_data = super(TicketForm, self).clean()

    gotten_phone_number = cleaned_data.get('phone_number')

    # Check if phone number begins with the Rwandan country code
    if gotten_phone_number[:4] == '+250':
    
        # print('country code detected')

        # Convert string to phone number
        string_to_phonenumber = phonenumbers.parse(gotten_phone_number, "RW")

        print(len(gotten_phone_number))

        # Check if the phonenumber is not a valid Rwandan number
        if phonenumbers.is_possible_number(string_to_phonenumber) != True or len(gotten_phone_number) != 13:
          
            # print('Not a valid Rwandan number')
            raise forms.ValidationError('The phone number is not a valid Rwandan phone number')
    
    # Check if the number begins with a 0
    elif gotten_phone_number[:2] == '07':
    
        # print('number without country code')
        
        # Phone number string without 0
        without_zero = gotten_phone_number[1:]
        
        # Add Rwandan country code to the beginning
        add_country_code = '+250' + without_zero

        # Convert string to phone number
        string_to_phonenumber = phonenumbers.parse(add_country_code, "RW")

        # Check if the phonenumber is not a valid Rwandan number
        if phonenumbers.is_possible_number(string_to_phonenumber) != True or len(add_country_code) != 13:
            
            # print('Not a valid Rwandan number')
            raise forms.ValidationError('The phone number is not a valid Rwandan phone number')

    # Otherwise
    else:
      
        # print('number with non-Rwandan country code')
        raise forms.ValidationError('The phone number is not a valid Rwandan phone number')

    return cleaned_data

class DateInput(forms.DateInput):
    input_type = 'date'



        
class ScheduleForm(forms.ModelForm):
  class Meta:
    model = Schedule

    fields = ('name','departure_location','destination_location', 'price', 'date','departure_time')
    widgets = {
            'date': DateInput(), 'departure_time' : forms.Select(choices=HOUR_CHOICES)
        }
  