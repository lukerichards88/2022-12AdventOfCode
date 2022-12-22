with open('ordered.txt', 'r') as file:
    for line in file:
        exec(line.strip(), globals())
        variable = line.split(' ')[0]
        if variable == 'humn':
            with open('evaluated.txt', 'a') as file:
                file.write(line + "\n")
        else:
            instructionOne = f"line = f'{variable} = " + "{" + variable + "}\\n'"
            exec(instructionOne, globals())
            with open('evaluated.txt', 'a') as file:
                file.write(line)

        print(instructionOne)