with open('day2/input.txt', 'r') as file:
    input = file.read().strip()

idranges = input.split(",")

invalid_sum = 0

for idrange in idranges:
    line = idrange.split("-")
    begin = int(line[0])
    end = int(line[1])

    for id in range(begin, end + 1):
        id = str(id)
        firsthalf = id[0:int((len(id)/2))]
        secondhalf = id[int((len(id)/2)):]
        if (len(id) % 2 == 0) and firsthalf == secondhalf:
            invalid_sum += int(id)

print(invalid_sum)

                    