#!/usr/bin/python3
import sys
import yaml
import math
from datetime import datetime
from datetime import timedelta
from pprint import pprint
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

months = mdates.MonthLocator((1, 4, 7, 10))
weeks = mdates.YearLocator()
months_fmt = mdates.DateFormatter('%b\'%y')


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

    balance_dates = [ ]
    payment_dates = [ ]
    payments = [ ]
    balances = [ ]

    while True:
      
      if projected_date.day == payment_day:
        payment_dates.append(projected_date)
        paid += payment_amount

        # apply payment
        updated_accrued_interest = math.ceil((accrued_interest - payment_amount) * 100.0) / 100.0

        if updated_accrued_interest >= 0:
          accrued_interest = updated_accrued_interest
          payments.append(paid)
        else:
          accrued_interest = 0
          updated_principal = math.ceil((principal + updated_accrued_interest) * 100.0) / 100.0
          if updated_principal > 0:
            principal = updated_principal
            payments.append(paid)
          else: # done paying
            balance = principal + accrued_interest
            principal = 0
            paid -= abs(updated_principal)
            payments.append(paid)
            balance_dates.append(projected_date)
            balances.append(balance)

            print('Projected to complete payment by', projected_date.strftime('%Y-%m-%d'))
            print(f'You will have paid a total of ${paid:.2f}.')
            print(f'On date of final payment, you need only pay ${(payment_amount - abs(updated_principal)):.2f} of the scheduled ${payment_amount:.2f}.')
            break
      
      balance = math.ceil((principal + accrued_interest)*100.0) / 100.0 # update balance

      balance_dates.append(projected_date)
      balances.append(balance)
      projected_date += timedelta(days=1) # increment day

      # update days in year after new year
      if projected_date.month == 1 and projected_date.day == 1:
        days_in_year = (datetime(projected_date.year + 1, 1, 1) - datetime(projected_date.year, 1, 1)).days
      
      accrued_interest = math.ceil((accrued_interest + (rate / days_in_year)*principal)*100.0) / 100.0  # accrue interest

    fig, ax = plt.subplots()
    ax.plot(balance_dates, balances, label='Balance')
    ax.plot(payment_dates, payments, 'ro', label='Payment Total')
    ax.xaxis.set_major_locator(months)
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.2f}'))
    ax.xaxis.set_major_formatter(months_fmt)
    ax.xaxis.set_minor_locator(weeks)
    ax.set_xlim(balance_dates[0], balance_dates[-1])
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    ax.set_xlabel('Date')
    ax.set_ylabel('USD')
    ax.set_title('Projected Student Loan Repayment', fontsize=14, fontweight='bold')

    starting_date = balance_dates[0].strftime("%d %b'%y")
    ax.annotate(f'Starting Balance (${balances[0]:,.2f} on {starting_date})', xy=(balance_dates[0], balances[0]), xytext=(balance_dates[round(len(balance_dates)*.04)], 1.07*balances[0]), arrowprops=dict(facecolor='black', shrink=0.005, width=2), fontweight='bold')
    final_date = payment_dates[-1].strftime("%d %b'%y")
    ax.annotate(f'Grand Total (${payments[-1]:,.2f} on {final_date})', xy=(payment_dates[-1], payments[-1]), xytext=(payment_dates[round(len(payment_dates)*.74)], 0.73*payments[-1]), arrowprops=dict(facecolor='black', shrink=0.005, width=2), fontweight='bold')

    ax.legend(loc='upper center')
    ax.grid(True)
    fig.autofmt_xdate()


if __name__ == "__main__":
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
