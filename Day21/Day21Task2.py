from sympy import symbols, solve

filename = 'ordered.txt'

def main():
    NameErrors = True
    while NameErrors:
        NameErrors = False
        with open(filename) as file:
            for line in file:
                line = line.strip().replace(':', ' =')
                try:
                    exec(line.strip(), globals())
                except NameError:
                    NameErrors = True
    print(mcnw)
    return root


if __name__ == "__main__":
    print(main())
