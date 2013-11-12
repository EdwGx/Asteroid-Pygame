#chemistry.py

def getSymbol(Atomic_number):
    return {
        1: "H",
        2: "He",
        3: "Li",
        6: "C",
        8: "O",
        13: "Al",
        18: "Ar"
    }[Atomic_number]

def get_shells(Atomic_number):
    return {
        1: [1],
        2: [2],
        3: [2,1],
        6: [2,4],
        8: [2,6],
        13: [2,8,3],
        18: [2,8,8]
    }[Atomic_number]

def freeFall(time_after,start_y):
    return int((start_y + (9.81* time_after * time_after / 100000)))
    
    
