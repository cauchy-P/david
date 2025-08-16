def solution(t, p):
    l= len(t)-len(p)+1
    ss = [t[i:i+len(p)] for i in range(l)]
    #print(ss)
    return len(list(filter(lambda x : int(x[0]) <= int(x[1]), zip(ss, [p]*l))))

solution("10203", "15")