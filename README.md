## Bias Random Walk Generator

This repository contains the code of bias random walk generator which integrates [node2vec](https://github.com/aditya-grover/node2vec) and [BiNE](https://github.com/clhchtcjj/BiNE).



### Environment settings

- python == 3.5
- networkx == 1.11
- numpy == 1.13.3



### Basic Usage

**Main Parameters**

```
Input graph path. Default is 'data/graph.dat'.(--input)
Prefix name of walks path. Defult is 'data/walks'.(--output)
maxT. Default is 128. (--maxT)
minT. Default is 1. (--minT)
Return hyperparameter. Default is 1. (--p)
Inout hyperparameter. Default is 1. (--q)
Stop walking hyperparameter. Default is 0.15. (--p_stop)
Metrics of centrality. Default is hits. (--mode)
Boolean specifying (non-)bipartite. Default is non-bipartite. (--bipartite)
Boolean specifying (un)weighted. Default is unweighted. (--weighted)
Graph is (un)directed. Default is undirected. (--directed)
```

**Usage**

We provide one process dataset **[Windsurfers](http://konect.uni-koblenz.de/networks/moreno_beach)**. This undirected network contains interpersonal contacts between windsurfers in southern California during the fall of 1986. A node represents a windsurfer and an edge between two windsurfers shows that there was a interpersonal contact.

- graph dataset ./data/graph.dat

Please run the './main.py'

```
python main.py --input data/graph.dat --output data/walks --weighted --p_stop 0.05
```

The walks are saved in the file './data/walks.dat'.



### Example

**Run**

```
python main.py --input data/graph.dat --output data/walks --weighted --p_stop 0.05
```

**Output**

```
Walking...
```

**Walks**

```
11 13 12 1 16 38 39 29 41
5 19 4 2 20 5 3 2 32 36 38 34 36 43 9 38 35 36 38 35 34 43 38 36 9 16 36 38 43 38 9 1 5 4 5 20 3 2 3 5 2 5 10 4 19 6 21 19 20 19 18
3 22 27 3 20 29 42 39 38 43 35 29 7 29 41 39 7 11 12 1 3 19
4
19 30 31 6
19 3 22 3 20
35 43 38 10 36 34 36 38 36 35 38 11 12 3 36 35 19 26 19 22 19 3 2
29 30 42 31 34 36
6 3 9 43 36
3 19 3 2 5 2
....
```



