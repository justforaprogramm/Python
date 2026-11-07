import numpy as np 
from math import sqrt
def main() -> None:
    calc_type = input('vector or points? (v, p):')
    
    match calc_type:
        case 'v':
            lst1 = list(map(float, input('give first vector (x1, x2, x3):').split(', ')))
            lst2 = list(map(float, input('give second vector (x1, x2, x3):').split(', ')))
            print(vector_given(lst1, lst2))
        case 'p':
            p1 = list(map(float, input('give first point (x1, x2, x3):').split(', ')))
            p2 = list(map(float, input('give second point (x1, x2, x3):').split(', ')))
            p3 = list(map(float, input('give third point (x1, x2, x3):').split(', ')))
            print(point_given(p1, p2, p3))
        case _:
            print('not v or p')


def point_given(p1:list[float], p2:list[float], p3:list[float]) -> str:
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)

    pA = p2 - p1
    pB = p3 - p1
    return vector_given(pA, pB)

def vector_given(lst1:list[float], lst2:list[float]) -> str:
    res:float = 0
    resVectr = np.cross(lst1, lst2)
    
    for num in resVectr:
        res += num**2

    return f'surface area: {sqrt(res)*0.5}'

if __name__ == '__main__':
    main()