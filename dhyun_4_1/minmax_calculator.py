if __name__ == "__main__":
    numberlist = sorted(list(map(float,input("Enter a mathematical expression: ").split(' '))))
    print("Min: %.2f, Max: %.2f" % (numberlist[0], numberlist[-1]))
