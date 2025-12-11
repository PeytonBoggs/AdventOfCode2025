import functools

file = open("day11/input.txt", "r")

devices = {}
for line in file:
    device = line.strip().split(":")
    input = device[0]
    output = device[1].split()
    devices.update({input: output})

# This solution assumes no infinite loops

@functools.cache
def get_fft_dac_paths(input, seen_fft, seen_dac):
    outputs = devices.get(input)

    if input == "fft":
        seen_fft = True
    if input == "dac":
        seen_dac = True

    if 'out' in outputs:
        if seen_fft and seen_dac:
            return 1
        else:
            return 0
    else:
        num_ftt_dac_paths = 0
        for output in outputs:
            num_ftt_dac_paths += get_fft_dac_paths(output, seen_fft, seen_dac)
        return num_ftt_dac_paths

print(get_fft_dac_paths("svr", False, False))
