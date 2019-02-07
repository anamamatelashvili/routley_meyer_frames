# Routley-Meyer Frames


#### Table of Contents
1. [Introduction](#introduction)
2. [Instructions](#instructions)
3. [Files](#files)


### Introduction
In this project we implement Routley-Meyer frames used for relevance logic (see section 3.7 of [this article](https://consequently.org/papers/rle.pdf)). 

The frames are triples <S, P, R> where:
* S = n = {0, 1, 2, ... , n-1} with n > 0, 
* P is a nonempty subset of S, 
* and R is a subset of S^3. 
        
Definitions:
* a≤b means there exists x in P with Rxab
* R^2 abcd means there exists x in S with (Rabx & Rxcd)
* R^2 a(bc)d means there exists x in S with (Raxd & Rbcx)

Frames need to satisfy the following for all a, b, c, a', b', c' in S:
* a≤a
* a≤b and b≤c => a≤c
* a’≤a and Rabc => Ra’bc
* b’≤b and Rabc => Rab’c
* c≤c’ and Rabc => Rabc’

### Instructions
1. Run `python rmframe.py` in the project's root directory to see an example of a frame with its attributes and some of its methods as well as an example of `get_frames` function.

2. You can `import rmframe` and make your own frame. You can use the following to get started with a frame example:

    - `R1 = [(0,0,0), (0,1,1), (0,2,2), (1,0,1), (1,1,0), (1,1,1), (1,1,2), (1,2,1), (1,2,2), (2,0,2), (2,1,1), (2,1,2), (2,2,0), (2,2,1), (2,2,2)]`
    - `frame = rmframe.RMFrame(R = R1, P = [0], n = 3)` 
    - `frame.r(0,1,1)` checks if (0,1,1) is in R (True)
    - `frame.r_S(0,1)` checks if 0≤1 for ≤ defined above (False) 
    - `frame.r2_1(a, b, c, d)` and `frame.r2_2(a, b, c, d)` check if (a,b,c,d) satisfy the two versions of R^2 defined above
    - `frame.draw_table()` draws R in a table form
    - `frame.set_closure({0,1})` returns the set of all elements of S that are smaller than anythin in {0,1} ({0,1})
    - `frame.get_quadruples1()` and `frame.get_quadruples2()` return all quadruples (a,b,c,d) that satisfy the two versions of R^2
    - `get_frames(n=3, tries = 100000)` will try to find new frames among all possibilities of <S, P, R> with S = 3 = {0,1,2}, but it will only try the first 100000 possibilities (with random R sizes)

### Files
The repository contains the following files:

* rmframe.py -- contains the code for the frame class and auxiliary functions 
