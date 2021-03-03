hours=input('Enter the number of hours worked this week: ')
hours=int(hours)
rate=10
pay=hours*rate
ot_rate=15
ot_hours=hours>40
ot_pay=ot_rate*ot_hours
if hours<=40:
    print('Wages for this week:', pay)
else:
    print('Wages for this week including overtime pay:', pay+ot_pay)
    print('Thank you for your extra effort - great job!')
print('Enjoy your weekend!')
