import csv

with open('BloodPressure.csv', mode='w') as csv_file:
    fieldnames = ['blood_pressure']
    for x in range(70,191):
        for y in range(40,101):
            bp = "%d/%d mmHg"%(x,y)
            csv_file.write(bp + ",")
    

    
    
    