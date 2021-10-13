#!/usr/bin/env python3

import random
import math
import matplotlib.pyplot as plt
import timeit
import os
import functools
import concurrent.futures as future
from time import perf_counter as pc
from multiprocessing import cpu_count

class MCC:
    def __init__(self, n=10):
        """
            Creates an MCC object (Monte Carlo Circle) that holds all points. 
            Points can be accessed as: 
            MCC.points[0][i] for X coordinate
            MCC.points[1][i] for Y coordinate
        """
        self.points = [ (0, 0) for _ in range(n) ]
        for i in range(n):
            self.points[i] = ( random.uniform(-1, 1), random.uniform(-1, 1) )
    
    def pic(self):
        """
            pic = Points In Circle
        """
        pic = []
        for point in self.points:
            if point[0] ** 2 + point[1] ** 2 < 1:
                pic.append(( point[0], point[1] ))
        return pic
    
    def poc(self):
        """
            poc = Points Outside Circle
        """
        poc = []
        for point in self.points:
            if point[0] ** 2 + point[1] ** 2 > 1:
                poc.append(( point[0], point[1] ))
        return poc

def main_1_1():
    numbers = [ 1000
              , 10000
              , 100000
              , 1000000
              ]
    plots = []
    for n in numbers:
        starttime = timeit.default_timer()
        mcc = MCC(n)
        points_in  = mcc.pic()
        points_out = mcc.poc()
        pic = len(points_in)
        poc = len(points_out)
        print("-----")
        print(f"Points generated: {n}")
        print(f"Points in circle: {pic}")
        print(f"Pi approximation: {4 * pic / n}")
        print(f"Execution time  : {round((timeit.default_timer() - starttime)*1000)/1000} seconds")
        
        coord_in = list(zip(*points_in))
        coord_out = list(zip(*points_out))
        fig = plt.figure(figsize=(8,8), dpi=144)
        plt.plot( coord_in[0]
               , coord_in[1]
               , 'r.'
               , label='Points inside circle'
               )
        plt.plot( coord_out[0]
               , coord_out[1]
               , 'b.' 
               , label='points outside circle'
               )
        plt.title(f"Monte Carlo $\pi$ie, n = {n}, $\pi$ = {4 * pic / n}", fontsize=16, fontweight='bold')
        plt.xlabel("X coordinate")
        plt.ylabel("Y coordinate")
        plt.legend()
        fig.tight_layout()
        fig.savefig(f"Uppg1_1{os.sep}Montecarlopie_{n}.png")

class MCHS:
    def __init__(self, n=100, d=3):
        """
            Creates a Monte Carlo Hypersphere that holds all points. 
            n is number of points
            d is number of dimensions
        """
        self.num = n
        self.dim = d
        self.points = [ list(range(d)) for _ in range(n) ] # List comprehension
        for num in range(n):
            for dim in range(d):
                self.points[num][dim] = random.uniform(-1, 1)
    
    def pihs(self):
        """
            Method returns a list of all points inside of the hypersphere. 
            pihs = Points Inside HyperSphere
        """
        pihs = []
        for point in self.points:
            sum = functools.reduce(lambda a, b: a + b, map(lambda x: x**2, point)) # This is definitely not the most readable way to do this, but it's lambda functions and map() and functools.reduce(). 
            if sum < 1:
                pihs.append(point)
        return pihs
    
    def mcvol(self):
        """
            Calculates the volume of the hypersphere numerically using a monte carlo method for the given MCHS object
        """
        return len(self.pihs()) / len(self.points) * 2 ** self.dim
    
    def anvol(self):
        """
            Calculates the volume of the hypersphere analytically for the given MCHS object
        """
        return math.pi ** (self.dim / 2) / math.gamma( self.dim / 2 + 1 )

def main_1_2():
    for d in [2, 11]:
        mchs = MCHS(100000, d)
        print(f"Hypersphere in {mchs.dim} dimensions, n = {mchs.num}")
        print(f"Approximated volume: {mchs.mcvol()}")
        print(f"Exact volume       : {mchs.anvol()}")

def hsvol(dim):
    """
        Calculates the volume of a hypersphere of dimension dim and radius 1 analytically
    """
    return math.pi ** (dim / 2) / math.gamma( dim / 2 + 1 )

def hsvol_mc_mt(threads, n=1000, dim=11):
    """
        Multi-threaded calculation of the volume of a hypersphere using monte-carlo methods
    """
    res = 0
    n_threads = list(map( lambda x: int(n/threads), list(range(threads)) ))
    if n%threads != 0: 
        n_threads[len(n_threads)-1] += n % threads
    tasks   = list(range( threads ))
    results = []
    with future.ProcessPoolExecutor() as ex:
        results_map = ex.map(_hsvol_mc_mt, n_threads)
        for result in results_map: results.append(result)
    return sum(results)/len(results)

def _hsvol_mc_mt(n=1000, dim=11):
    mchs = MCHS(n, dim)
    return mchs.mcvol()
        

def main_1_3():
    n = 100000
    n = 10000000 # This is the desired number
    start = pc()
    mchs = MCHS(n, 11)
    print("--- Single-thread execution ---")
    print(f"Hypersphere in {mchs.dim} dimensions, n = {mchs.num}")
    print(f"Approximated volume: {mchs.mcvol()}")
    print(f"Exact volume       : {hsvol(mchs.dim)}")
    stop = pc()
    print(f"Execution time     : {stop-start} seconds")
    print()
    
    threads = 10
    start = pc()
    # Important difference: multithreading is sent to a separate function, since population of the random MCHS object takes significant time for large values of n.     
    print(f"--- {threads}-thread execution ---")
    print(f"Hypersphere in 11 dimensions, n = {n}")
    print(f"Approximated volume: {hsvol_mc_mt(threads, n)}")
    print(f"Exact volume       : {hsvol(11)}")
    stop = pc()
    print(f"Execution time     : {stop-start} seconds")
    print()
    
    # n = 1000000
    print(f"--- How many threads are sensible, really? ---")
    print(f"This system runs on {cpu_count()} processor cores. Are more threads than cores beneficial?")
    print(f"Hypersphere in 11 dimensions, n = {n}")
    times = []
    for threads in range( 1, cpu_count() + int(cpu_count()/2) + 1 ):
        print(f"Threads  : {threads}")
        start = pc()
        hsvol_mc_mt(threads, n)
        time = pc() - start
        times.append(time)
        print(f"Exec time: {time}")
    fig = plt.figure(figsize=(8,8), dpi=144)
    plt.plot( range(1, len(times)+1)
            , times
            )
    plt.title(f"Execution time depending on number of threads")
    plt.xlabel(f"Number of threads, system has {cpu_count()} cores")
    plt.ylabel("Execution time, seconds")
    fig.tight_layout()
    fig.savefig(f"Exectimes_n={n}_cores={cpu_count()}.png")
    

if __name__ == '__main__':
    print("Hello world!")
    print("MA4 1.1: First, let's do some pi-approximations!")
    main_1_1()
    print()
    print("MA4 1.2: Now, some hyperspheres! This is where math goes weird.")
    main_1_2()
    print()
    print("MA4 1.3: Time for parallel programming, useful on hyperspheres!")
    main_1_3()
