import os

for x in range(5, 25):
    day = f"Day{x}"
    os.mkdir(day)
    for y in range(1, 3):
        task = f"Task{y}"
        filename = f"{day}/{day}{task}.py"
        with open(filename, 'w') as file:
            file.write("\n")
