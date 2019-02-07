from functools import reduce
from itertools import product, combinations
import numpy as np
import pandas as pd


def rel3(R, a, b, c):
    return ((a,b,c) in R)
        
def rel2RP(R, P, a, b):
    return any({rel3(R,x,a,b) for x in P})

def subsets(s):
    cardinalities = np.random.permutation(len(s) + 1)
    for cardinality in cardinalities:
        yield from combinations(s, len(s) - cardinality)


class RMFrame:
    
    def __init__(self, R, P, n):
        """
        The frames are triples <S, P, R> where:
            S = n = {0, 1, 2, ... , n-1} with n > 0, 
            P is a nonempty subset of S, 
            and R is a subset of SxSxS. 
        
        Definitions:
        a≤b = \exists x\in P Rxab
        R^2 abcd = \exists x(Rabx & Rxcd)
        R^2 a(bc)d = \exists x(Raxd & Rbcx)

        Frames need to satisfy the following.
        a≤a
        a≤b and b≤c => a≤c
        a’≤a and Rabc => Ra’bc
        b’≤b and Rabc => Rab’c
        c≤c’ and Rabc => Rabc’
        """
        self.S = n
        self.P = P
        self.R = R
        
    @property
    def S(self):
        return self.__S

    @S.setter
    def S(self, s):
        if not s: raise Exception("S must be non-empty (>0)")
        if (hasattr(self, 'P') and hasattr(self, 'R')): 
            self.__S = set(range(s))
            self.P = self.P
            self.R = self.R
        self.__S = set(range(s))
    
    @property
    def P(self):
        return self.__P

    @P.setter
    def P(self, p):
        if not set(p): raise Exception("P must be non-empty")
        if not (set(p).issubset(self.S)): raise Exception("P must be a subset of S")
        if hasattr(self, 'R'): 
            self.__P = set(p)
            self.R = self.R    
        self.__P = set(p)

    @property
    def R(self):
        return self.__R

    @R.setter
    def R(self, rr):
        if not (set(rr).issubset(set(product(self.S, repeat = 3)))): raise Exception("R must be a subset of S3")
        if any({not rel2RP(set(rr), self.P, a, a) for a in self.S}): raise Exception("We should have a≤a for all a in S")
        if any({(rel2RP(set(rr), self.P, a, b) and rel2RP(set(rr), self.P, b, c) and not rel2RP(set(rr), self.P, a, c)) 
               for a in self.S
               for b in self.S
               for c in self.S}): raise Exception("We should have a≤b and b≤c => a≤c for all a, b and c in S")
        if any({(rel2RP(set(rr), self.P, a1, a) and rel3(set(rr), a, b, c) and not rel3(set(rr), a1, b, c)) 
               for a in self.S
               for a1 in self.S
               for b in self.S
               for c in self.S}): raise Exception("We should have a'≤a and Rabc => Ra'bc for all a, a', b and c in S")   
        if any({(rel2RP(set(rr), self.P, b1, b) and rel3(set(rr), a, b, c) and not rel3(set(rr), a, b1, c)) 
               for a in self.S
               for b1 in self.S
               for b in self.S
               for c in self.S}): raise Exception("We should have b’≤b and Rabc => Rab’c for all a, b, b' and c in S")
        if any({(rel2RP(set(rr), self.P, c, c1) and rel3(set(rr), a, b, c) and not rel3(set(rr), a, b, c1)) 
               for a in self.S
               for c1 in self.S
               for b in self.S
               for c in self.S}): raise Exception("We should have c≤c’ and Rabc => Rabc' for all a, b, c and c' in S")    
        self.__R = set(rr) 
        
    def r(self, a, b, c):
        return ((a,b,c) in self.R)
        
    def r_S(self, a, b):
        return any({self.r(x,a,b) for x in self.P})
    
    def r2_1(self, a, b, c, d):
        return any({(self.r(a,b,x) and self.r(x,c,d)) for x in self.S})
        
    def r2_2(self, a, b, c, d): 
        return any({(self.r(a,x,d) and self.r(b,c,x)) for x in self.S})
   
    def draw_table(self):
        indices = list(self.S)
        indices.sort()
        table = pd.DataFrame(index=indices, columns=indices)
        table = table.fillna('')
        for a in indices:
            for b in indices:
                for c in indices:
                    if self.r(a,b,c):
                        table.loc[a,b] = table.loc[a,b] + str(c)
        print("P: ", self.P)
        print("R: ")
        print(table)                
      
    def set_closure(self, sub_set):
        return {a for a in self.S if any({self.r_S(a,x) for x in sub_set})}
    
    def get_closed_subsets(self): 
        sub_sets = [set(sub_set) for sub_set in subsets(self.S) if set(sub_set) == self.set_closure(set(sub_set))]
        print('There are {} closed subsets of S:'.format(len(sub_sets)))
        print(sub_sets)
        return sub_sets
    
    def get_quadruples1(self):
        quads1 = [(a,b,c,d) for a, b, c, d in set(product(self.S, repeat = 4)) if self.r2_1(a,b,c,d)]
        print(quads1)
        return quads1
        
    def get_quadruples2(self):   
        quads2 = [(a,b,c,d) for a, b, c, d in set(product(self.S, repeat = 4)) if self.r2_2(a,b,c,d)]
        print(quads2)
        return quads2  
        
    
    
def get_frames(n, tries = None):
    S = set(range(n))
    S3 = set(product(S, repeat = 3))
    frames = []
    if tries: i = 0
    for R in subsets(S3):
        if tries: 
            if i >= tries: break
        for P in subsets(S):
            try: frames.append(RMFrame(R=set(R), P=set(P), n=n))
            except: pass
            if tries: 
                i += 1
                if i >= tries: break 
    if tries:
        print('There are {} frames for n = {} for the first {} tries.'.format(len(frames), n, tries))
    else:
        print('There are {} frames for n = {}.'.format(len(frames), n))
    return frames     
    
    
    
    
    
if __name__ == "__main__":    
    R1 = [(0,0,0), (0,1,1), (0,2,2), (1,0,1), (1,1,0), (1,1,1), (1,1,2), (1,2,1), (1,2,2), (2,0,2), (2,1,1), (2,1,2), (2,2,0), (2,2,1), (2,2,2)]
#    R2 = [(0,1,1), (0,2,2), (1,0,1), (1,1,0), (1,1,1), (1,1,2), (1,2,1), (1,2,2), (2,0,2), (2,1,1), (2,1,2), (2,2,0), (2,2,1), (2,2,2)]
    
    print('Example of a frame:')
    frame1 = RMFrame(R = R1, P = [0], n = 3)
    print('Attribute P: ', frame1.P)
    print('Attribute S: ', frame1.S)
    print('Attribute R: ', frame1.R)
    print()
    print('Example of draw_table method:')
    frame1.draw_table()
    print()
    print('Example of get_closed_subsets method:')
    frame1.get_closed_subsets()
    print()
    print('Example of get_quadruples1 and get_quadruples2 methods:')
    frame1.get_quadruples1()
    frame1.get_quadruples2()
    
    print()
    print('Example of get_frames function:')
    frames = get_frames(n=3, tries = 100000)
    for frame in frames:
        frame.draw_table()