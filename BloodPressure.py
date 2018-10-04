import csv

with open('CSV/BloodPressure.csv', mode='wb') as csv_file:
    fieldnames = ['blood_pressure']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    for x in range(70,191):
        for y in range(40,101):
            bp = "%d over %d mmHg"%(x,y)
            writer.writerow({'blood_pressure': bp})
    