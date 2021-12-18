Day 6 Graph distance, Poset formation, "topological ordering" I think?

Represent a graph as a matrix A, A^2[0][1] = n => 0 and 1 have n neighbors in common. Equivalently, there are n distinct 
paths of length 2 from 0 to 1. So A^2[0] = the degree of 0.

Represent a directed acyclic graph G as a matix A. A*[0][1] > 0 iff there is a path "forwards" from 0 to 1. How to construct 
the full partially-ordered set P = {a<z : there exists a chain a<b...y<z such that each step a<b... is in the dag}. It's 
possible to do it in |G|^2 time in "one pass" through G.

We construct dictionaries: lt and gt such that for each b in G, lt[b] is a list of all elements in G which are less than b and 
gr is a list of all elements of G which are greater than b. Initialize lt and gt with the successors in G, i.e., add to lt[b] 
all e in G such that "e<b" is in G and add to gt[b] all e in G such that "b<e" is in G.

for b in G:
    for each a in lt[b]
        for each c in gt[b]
            add a to lt[c] and add c to gt[a]

If there is a path a<b<c<d<e<f<g in the matrix, suppose that the elements appear randomly as d,b,e,g,a,f,c. When d appears, we 
learn c<e. When b appears, we learn a<c. Wheen e appears, we learn c<f. When g appears, we learn nothing. When a appears, we 
learn nothing. When f appears, we learn c<g. When c appears, we learn a<g. I.e., we learn a<g after adding the elements of the 
chain a...g in any order.
