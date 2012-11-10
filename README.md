# Preamble

Simulation of the gravitational attraction and motion of "stars" in a 2d universe.

This whole project is really an excuse to try out some neat algorithms and build some fun stuff from scratch.

Until I find the time to write a humongous, detailed readme: there are docstrings a-plenty in these files, and they should give an idea of what everything does. 

# Description of the Underlying Problem
The gravitational attraction between N stars can be most easily computed in O(N^2) time with the following algorithm:
    
    for each of the N stars:
        calculate gravity with the other (N-1) stars

The purpose of this project is to find an accurate way to compute the gravitational attraction between N stars in sub-quadratic time. This will rely on the simplification that a group of stars can be approximated as a single large star, as long as this group is far enough away. The algorithm then looks something like this:

    for each of the N stars: 
        calculate gravity with the nearest k stars
        group farther stars into m clusters, and calculate gravity with each of the clusters

This requires O( N*(k+m) ) gravity calculations. Assuming that we can use constant k and m proportional to log(N), then the algorithm requires roughly O(N*logN) calculations; a significant improvement. 

## Choosing a Data Structure
An ideal data structure to hold the positions of the stars would allow us to:

1. quickly find the k nearest stars to a point P (or alternatively, all stars within a distance L to a point P)
2. quickly group faraway stars into O(logN) clusters, and for each cluster find an appropriate approximation of the cluster as a single star.

The solution is a structure where the N stars are divided into q partitions (q=2 or q=4, probably) and each of the q partitions are recursively divided into q partitions until the smallest partitions contain less than. This results in a tree structure where points closer together in the tree are likely to be closer together in real space. 

R trees, k-d trees, vp trees, and quadtrees were all considered

### Quadtrees
Quadtrees seem efficient, providing a good balance between overhead (tree maintenance) and search speed. 