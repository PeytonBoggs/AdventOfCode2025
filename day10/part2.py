import re
import scipy

file = open("day10/input.txt", "r").readlines()

machines = []
# Process machine
for line in file:
    line = line.strip().split()

    # Process buttons
    buttons = []
    for b in range(1, len(line) - 1):
        button = []
        nums = re.findall("[0-9]", line[b])
        for num in nums:
            button.append(int(num))
        buttons.append(button)

    # Process joltages
    str_required_joltages = (line[len(line) - 1][1:len(line[len(line) - 1]) - 1]).split(",")
    required_joltages = []
    for joltage in str_required_joltages:
        required_joltages.append(int(joltage))
            
    machine = [buttons, required_joltages]
    machines.append(machine)

total_presses = 0

# Get the number of buttons presses for each machine
for machine in machines:
    # Create button matrix for processing
    button_matrix = [[0 for _ in range(len(machine[0]))] for _ in range(len(machine[1]))]
    for i, button in enumerate(machine[0]):
        for joltage_affected in button:
            button_matrix[joltage_affected][i] = 1

    # Arrays to be used in optimization
    buttons = [1 for _ in range(len(machine[0]))]
    required_joltages = machine[1]

    # Contraint on optization; the pushed buttons mmust equal the required joltages
    constraint = scipy.optimize.LinearConstraint(A=button_matrix, lb=required_joltages, ub=required_joltages)

    # Optimize the linear algebra problem Ax = b, using constraint, with all entries in x to be integers
    optimization = scipy.optimize.milp(buttons, integrality=1, constraints=constraint)
    
    numpresses = int(optimization.fun)
    total_presses += numpresses

print(total_presses)