filename = 'Day21Test.txt'
filename = 'Day21Input.txt'

def main():
    NameErrors = True
    while NameErrors:
        NameErrors = False
        with open(filename) as file:
            for line in file:
                line = line.strip().replace(':', ' =')
                try:
                    exec(line.strip(), globals())
                    with open('ordered.txt', 'a') as file:
                        file.write(line + "\n")
                except NameError as e:
                    NameErrors = True
    return root


if __name__ == "__main__":
    print(main())
