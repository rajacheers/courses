balance = 999999
annualInterestRate = 0.18

mon_int_rate = annualInterestRate/12.0

total = 0
low_bound = balance/12.0
up_bound = (balance*(1+mon_int_rate)**12)/12.0
min_mon_pay = (low_bound+up_bound)/2
print balance
while True:
    print "Min mon pay ",min_mon_pay
    
    prev_bal = balance
    for i in range(1,13):
        mon_unpaid_bal = prev_bal-min_mon_pay
        bal_each_month = mon_unpaid_bal+mon_int_rate*mon_unpaid_bal
        prev_bal = bal_each_month
    print "Balance ", prev_bal
    if prev_bal<-0.01:
        up_bound =  min_mon_pay
        
    elif prev_bal>0.01:
        low_bound = min_mon_pay
        
    else:
        break
    min_mon_pay = (low_bound+up_bound)/2
    
print("Lowest Payment: "+str(round(min_mon_pay,2))) 
