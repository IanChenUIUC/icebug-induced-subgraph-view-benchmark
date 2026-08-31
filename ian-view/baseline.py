"""Report the fixed memory offset the sweep starts from, for subtracting from timing CSVs."""

import numpy as np
import pyarrow.parquet as pq

import networkit as nk

import mem


def _read(col):
    return pq.read_table(f"../input/livejournal.{col}.parquet")[col].combine_chunks()


def main():
    nk.engineering.setNumberOfThreads(32)

    indptr, indices = _read("indptr"), _read("indices")
    n = len(indptr) - 1
    graph = nk.Graph.fromCSR(n, directed=False, out_indices=indices, out_indptr=indptr)

    distances = (
        nk.distance.BFS(graph, source=0, storePaths=False, storeNodesSortedByDistance=True)
        .run()
        .getDistances(asarray=True)
    )
    nodes = np.argsort(distances, kind="stable")

    print(f"n                {n}")
    print(f"nodes            {len(nodes)}")
    print(f"baseline_rss_mb  {mem.rss_mb():.1f}   subtract from peak_mb")


if __name__ == "__main__":
    main()
