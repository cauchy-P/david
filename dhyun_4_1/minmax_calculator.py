#The easy way

'''
if __name__ == "__main__":
    numberlist = sorted(list(map(float,input("Enter a mathematical expression: ").split(' '))))
    print("Min: %.2f, Max: %.2f" % (numberlist[0], numberlist[-1]))
'''
# The hard way

if __name__ == "__main__":
    try:
        numberlist = list(map(float,input("Enter a mathematical expression: ").split(' ')))
        # ["1" "3" "2" "5"] -> [1.0, 3.0, 2.0, 5.0]
    except ValueError:
        print("Invalid input.")
        exit(1)
    min_val = numberlist[0]
    max_val = numberlist[0]
    for n in numberlist:
        if n < min_val:
            min_val = n
        if n > max_val:
            max_val = n
    print("Min: %.2f, Max: %.2f" % (min_val, max_val))

