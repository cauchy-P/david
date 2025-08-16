def solution(bridge_length, weight, truck_weights):
    stk = []
    t = 0
    for truckw in truck_weights:
        if sum(stk) + truckw > weight or len(stk) == bridge_length:
            #print(stk)
            t += bridge_length + len(stk) - 1
            stk = []
            #print(t)
        stk.append(truckw)
    if stk:
        t += bridge_length + len(stk)
    return t
print(solution(2,10,[7,4, 5,6]))