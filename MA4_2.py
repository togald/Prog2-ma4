#!/usr/bin/env python3

""" MA4_2.py

Student:        Togald Nilsson
Mail:           togald.nilsson.1357@student.uu.se
Reviewed by:    Kellen Smith
Date reviewed:  2021-10-14
"""

from integer import Integer
from numba import njit
from time import perf_counter as pc
import matplotlib.pyplot as plt

def fib_py(n):
    if n <= 1:
        return n
    else:
        return(fib_py(n-1) + fib_py(n-2))

@njit
def fib_numba(n):
    if n <= 1:
        return n
    else:
        return(fib_numba(n-1) + fib_numba(n-2))

def fib_c(n):
    f = Integer(n)
    return f.fib()

def main():
    testrange = range(25, 35)
    print("Python, Numba and C++ comparisions! Yay! (also Linux things)")
    
    start = pc()
    for n in testrange: fib_py(n)
    print(f"Pure python: {pc() - start} sec")
    
    start = pc()
    for n in testrange: fib_numba(n)
    print(f"Numba      : {pc() - start} sec")
    
    start = pc()
    for n in testrange: fib_c(n)
    print(f"C++        : {pc() - start} sec")

def plotmaster_6000():
    testrange = range(30, 45)
    fs = [ fib_py, fib_numba, fib_c ]
    times = []
    for f in fs:
        times.append([])
        for n in testrange:
            start = pc()
            f(n)
            times[len(times)-1].append(pc()-start)
    fig = plt.figure(figsize=(7,5), dpi=144)
    plt.plot( testrange
            , times[0]
            , 'y.-'
            , label="Python"
            )
    plt.plot( testrange
            , times[1]
            , 'b.-'
            , label="Numba"
            )
    plt.plot( testrange
            , times[2]
            , 'r.-'
            , label="C++"
            )
    plt.title(f"Fibonacci numbers calculator performance", fontsize=16, fontweight='bold')
    plt.xlabel("Fibonacci number")
    plt.ylabel("Execution time, seconds")
    plt.legend()
    fig.tight_layout()
    plt.yscale('linear')
    fig.savefig(f"4_2.png")
    plt.yscale('log')
    fig.savefig(f"4_2_log.png")
    print()
    
def fib47():
    print("--- The dreaded 47th fibonacci number ---")
    start = pc()
    x = fib_numba(47)
    print(f"Numba takes: {pc() - start} sec")
    start = pc()
    y = fib_c(47)
    print(f"C++ takes  : {pc() - start} sec")
    print(f"To realize the 47th fibonacci number is {x} (Numba), {y} (C++)")

if __name__ == '__main__':
    main()
    plotmaster_6000()
    fib47()
