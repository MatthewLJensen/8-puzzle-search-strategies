# 8-puzzle-search-strategies
Implementing various search strategies to solve the 8-puzzle game including greedy best first search, A* search, and breadth first search.
I also compared these strategies using the rank function defined in 8PuzzleSearch.py. Here are those results:

## Comparison of Search Strategies and Heuristics
I tracked 3 values for each function and then averaged these values over 100 different random board positions. The random board positions were created by randomly moving an 8-puzzle instance 1000 times. I tracked the average number of visited nodes, the average number of steps in the solution, and the average time it took for the function to find the solution, in that order. Here are the results:

| Search Strategy                                         | Avg # of Visited Nodes  | Avg # Solution Steps  | Avg Secs to Solution |
| Breadth First Search                                    | 113927                  | 23.28                 | 1.002                |
| Greedy Best with 'Number of Tiles Displaced' Heuristic  | 1229                    | 91.18                 | 0.0095               |
| Greedy Best with 'Manhattan Distance' Heuristic         | 430.67                  | 62.46                 | 0.0044               |
| A* with 'Number of Tiles Displaced' Heuristic           | 24558.88                | 23.28                 | 0.21                 |
| A* with 'Manhattan Distance' Heuristic                  | 2716.05                 | 23.28                 | 0.028                |

### Comparing Search Strategies:
To evaluate the best search strategy, you have to decide on what to prioritize. If you want speed/fewer visited nodes, use greedy best first search. When compared with A* it found a solution while only visiting 5% of those nodes that A* did while using the number of tiles displaced heuristic, and 15.9% of the nodes that A* visited while using Manhattan distance heuristic. However, the length of the solution tended to be 3.92 times longer when using num displaced and 2.68 times longer when using Manhattan distance.
Breadth First search performed very poorly in regards to the total number of visited nodes. On average, it visited nearly 114,000 nodes to find a solution and took an average of 94.8 seconds to reach that solution. However, it always came up with an optimal solution, like A*.

So, if you are prioritizing speed, but not solution length, use greedy best first search. If you are prioritizing solution length, use A Star. Breadth first search only has a leg up on greedy best first search, because it finds an optimal path. But it takes far longer, averaging a full second to find the solution. Greedy best first search was 227 times faster, and A* was 36 times faster

### Comparing Heuristics:
Manhattan Distance finds a solution faster and with fewer visited nodes than the number of tiles displaced heuristic. When used in greedy BFS, num tiles displaced visited 2.85 times as many nodes as Manhattan distance, while coming up with a worse solution path. In the same comparison with A*, num tiles displaced visited 9.04 times as many nodes (with the same solution length, as finding an optimal path is a trait of A*). This shows that the Manhattan distance heuristic is superior to number of tiles displaced.

