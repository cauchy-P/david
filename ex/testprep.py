answers = [1,2,3,4,5]*2000
shot = [[1,2,3,4,5]*2000, [2,1,2,3,2,4,2,5]*1250, [3,3,1,1,2,2,4,4,5,5]*1000]
hit = [0,0,0]
for i in range(3):
    hit[i] = list(map(lambda x : bool(x[0]-x[1]), zip(shot[i], answers))).count(False)
print([i for i, x in enumerate(hit) if x == max(hit)])