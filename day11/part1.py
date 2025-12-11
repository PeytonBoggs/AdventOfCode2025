file = open("day11/input.txt", "r")

devices = {}
for line in file:
    device = line.strip().split(":")
    input = device[0]
    output = device[1].split()
    devices.update({input: output})

def get_out_paths(input):
    outputs = devices.get(input)

    if "out" in outputs:
        return 1
    else:
        num_out_paths = 0
        for output in outputs:
            num_out_paths += get_out_paths(output)
        return num_out_paths

print(get_out_paths("you"))
