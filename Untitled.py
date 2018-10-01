

file = open("temp.csv", "w")
temp = 0
while(temp < 50):
    file.write(str(round(temp,1))+" degrees \n")
    temp += 0.1

file.close()
    
