# About

This repository contains benchmarks for various implementations of induced subgraphs.
We use the livejournal dataset, symmetrized and cleaned to remove self-loops and multi-edges.

## Experiment

We create subgraphs of sizes 2^10, 2^{14}, 2^{18}, ... by taking BFS order from node 0.
For each of these, we run the following variants of induced subgraph:

1. `nk.graphtools.subgraphFromNodes` (main/gt.py)
2. `nk.graphtools.subgraphFromNodes(..., compact=True)` (main/gt_compact.py)
3. `nk.graph.InducedSubgraphView()` on a fork (ian-view/view.py)
4. `nk.graph.InducedSubgraphView(..., compact=True)` on a fork (ian-view/view_compact.py)
5. `nk.graph.InducedSubgraphView()` on the main branch (main/view.py)

We track the time it takes to build the subgraph, as well as run core decomposition afterwards.
Moreover, we track the memory usage (additional memory used to build subgraph and run core decomp).

All experiments are run with 32 threads, compiled using GCC 15.2.0 on AMD EPYC 7702 64-Core Processor.

## Results

![Timing](timing.pdf)
![Memory](mem.pdf)

Each subfigure shows the size of the induced subgraph that is created.
The methods are according to the order described above.

We see that on relatively smaller subgraphs (less than 20\% of the nodes), the fork's subgraph view using compact is the fastest.
On the largest case, where the subgraph is about 80\% of the nodes, the main branch's subgraph view is the fastest.
In general, for views, it is fast to construct the graph but slower to run an algorithm on it.

Regarding memory, the view with compact is always the smallest.
