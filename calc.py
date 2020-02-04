#!/usr/bin/python3
import sys
import yaml
import math
from datetime import datetime
from datetime import timedelta
from pprint import pprint

class Calculation:
  def __init__(self, params):
    self.principal = params.get('principal', None)
    self.rate = params.get('rate', None) # yearly rate
    self.accrued_interest = params.get('accrued_interest', None)
    payment_schedule = params.get('payment_schedule', None)
    if payment_schedule:
      self.payment_amount = payment_schedule.get('amount', None) # in dollars
      self.payment_day = payment_schedule.get('day', None) # in days
    self.start_date = params.get('start_date', None)

  def run(self):
    principal = self.principal
    rate = self.rate
    accrued_interest = self.accrued_interest
    payment_amount = self.payment_amount
    payment_day = self.payment_day
    start_date = datetime.strptime(str(self.start_date), '%Y-%m-%d') if self.start_date else datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    projected_date = start_date

    days_in_year = (datetime(projected_date.year + 1, 1, 1) - datetime(projected_date.year, 1, 1)).days

    paid = 0

    while True:
      
      if projected_date.day == payment_day:
        paid += payment_amount

        # apply payment
        updated_accrued_interest = math.ceil((accrued_interest - payment_amount) * 100.0) / 100.0

        if updated_accrued_interest >= 0:
          accrued_interest = updated_accrued_interest
        else:
          accrued_interest = 0
          updated_principal = math.ceil((principal + updated_accrued_interest) * 100.0) / 100.0
          if updated_principal > 0:
            principal = updated_principal
          else: # done paying
            balance = principal + accrued_interest
            principal = 0
            paid -= abs(updated_principal)

            print('Projected to complete payment by', projected_date.strftime('%Y-%m-%d'))
            print(f'You will have paid a total of ${paid:.2f}.')
            print(f'On date of final payment, you need only pay ${(payment_amount - abs(updated_principal)):.2f} of the scheduled ${payment_amount:.2f}.')
            break
      
      balance = math.ceil((principal + accrued_interest)*100.0) / 100.0 # update balance

      projected_date += timedelta(days=1) # increment day

      # update days in year after new year
      if projected_date.month == 1 and projected_date.day == 1:
        days_in_year = (datetime(projected_date.year + 1, 1, 1) - datetime(projected_date.year, 1, 1)).days
      
      accrued_interest = math.ceil((accrued_interest + (rate / days_in_year)*principal)*100.0) / 100.0  # accrue interest
    


try:
  filename = sys.argv[1]
except ValueError:
  print('No filename provided.  Assuming default "info.yml".')
  filename = 'info.yml'

with open(filename, 'r') as fs:
  params = yaml.safe_load(fs)

print('Running with following parameters:')
pprint(params)
print()

calc = Calculation(params)
calc.run()
