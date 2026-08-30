import time

import numpy as np
import pandas as pd
import pyarrow
import pyarrow.parquet as pq

import networkit as nk


def _read(col):
    return pq.read_table(f"../input/livejournal.{col}.parquet")[col].combine_chunks()


def main():
    nk.engineering.setNumberOfThreads(32)

    indptr, indices = _read("indptr"), _read("indices")
    n, m = len(indptr) - 1, len(indices) // 2
    graph = nk.Graph.fromCSR(n, directed=False, out_indices=indices, out_indptr=indptr)

    ## nodesets
    distances = (
        nk.distance.BFS(graph, source=0, storePaths=False, storeNodesSortedByDistance=True)
        .run()
        .getDistances(asarray=True)
    )
    nodes = np.argsort(distances, kind="stable")

    sizes, size = [], 1024
    while size <= n:
        sizes.append(size)
        size *= 4

    ## track the time for creating each View
    create_times = []
    decomp_times = []

    for size in sizes:
        print(f"creating subgraph view of size {size}")
        start = time.perf_counter()
        subg = nk.graphtools.subgraphFromNodes(graph, nodes[:size], compact=True)
        end = time.perf_counter()
        create_times.append(end - start)
        print(f"created subgraph view of n={size} m={subg.numberOfEdges()}")

        print("running core decomp on subgraph view")
        start = time.perf_counter()
        nk.centrality.CoreDecomposition(subg).run()
        end = time.perf_counter()
        decomp_times.append(end - start)

    columns = ["size", "create_time", "decomp_time"]
    data = []
    for size, create_time, decomp_time in zip(sizes, create_times, decomp_times):
        data.append([size, create_time, decomp_time])

    df = pd.DataFrame(data, columns=columns)
    df.to_csv("timing_gt_compact.csv", index=None)


if __name__ == "__main__":
    main()
