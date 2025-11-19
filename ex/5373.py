from collections import deque
cube = [[['r','r','r'], ['r','r','r'],['r','r','r']], #FRBLUD
        [['b','b','b'], ['b','b','b'],['b','b','b']],
        [['o','o','o'], ['o','o','o'],['o','o','o']],
        [['g','g','g'], ['g','g','g'],['g','g','g']],
        [['w','w','w'], ['w','w','w'],['w','w','w']], 
        [['y','y','y'], ['y','y','y'],['y','y','y']],
         ]
def rotatef():
    cube[4][2], list(zip(*cube[1])[0]), cube[5][0], cube[3][2]
    