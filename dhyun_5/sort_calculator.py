def msort(arr):
    l = len(arr)
    if l == 0: return []
    if l == 1: return arr
    elif l == 2: return arr if arr[0] < arr[1] else arr[::-1]
    else: 
        mid = l // 2
        left = msort(arr[:mid])
        right = msort(arr[mid:])
        return merge(left, right)
    
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def main():
    try:
        istr = input().split()
        numbers = list(map(float, istr))
        if not numbers:
            raise ValueError("No numbers provided")
    except ValueError:
        print("Invalid input")
        exit(1)

    print("Sorted :", *msort(numbers))

if __name__ == "__main__":
    main()