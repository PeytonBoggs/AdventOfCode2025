with open('day2/input.txt', 'r') as file:
    input = file.read().strip()

idranges = input.split(",")

invalid_sum = 0

for idrange in idranges:
    line = idrange.split("-")
    begin = int(line[0])
    end = int(line[1])

    for id in range(begin, end + 1):
        invalid = False
        id = str(id)

        for i in range(0, int((len(id)/2))):
            if id == id[0:i+1] * int((len(id) / (i+1))):
                invalid = True
                invalid_sum += int(id)
            if invalid:
                break

print(invalid_sum)

                    