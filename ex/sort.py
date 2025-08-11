def bsort(list):
	l = len(list)
	for i in range(l)[::-1]:
		for j in range(i):
			list[j], list[j+1] = (list[j+1], list[j]) if list[j] > list[j+1] else (list[j], list[j+1])
	return list
l = list(map(float, input().split()))
print(bsort(l))