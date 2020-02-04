# Student Loan Repayment Calculator

Calculates when you can expect to completely pay off your student loan balance with regular, fixed monthly payments.
Simply specify the following information in info.yml:

- Current\* principal balance
- Current accrued interest balance
- Annual percentage rate
- Payment schedule (fixed monthly amount and which day of the month you will be paying; should not be 29, 30, or 31 [too lazy to implement end of month])
- Start date (date before interest starts accruing)

An example is provided in info.yml with a current principal balance of **$10,000.00**, current accrued interest balance of **$2,000.00**, annual percentage rate of **20%**, payments scheduled for the **15** of each month at **$500.00**, starting **January 1st, 2020**.

\* *"Current" means the corresponding value at the start date, assuming interest has already accrued on that start date.*

---

## Example

See [example.ipynb](https://github.com/archwa/stuloan/blob/master/example.ipynb) for a working example.

**info.yml**
```yaml
principal: 10000.00
rate: 0.2
accrued_interest: 2000.00
payment_schedule:
  amount: 500
  day: 15
start_date: 2020-01-01
```

Setup and run program using:
```
make setup
source activate
make run
```

**output**
```
Running with following parameters:
{'accrued_interest': 2000.0,
 'payment_schedule': {'amount': 500, 'day': 15},
 'principal': 10000.0,
 'rate': 0.2,
 'start_date': datetime.date(2020, 1, 1)}

Projected to complete payment by 2022-07-15
You will have paid a total of $15129.65.
On date of final payment, you need only pay $129.65 of the scheduled $500.00.
```
