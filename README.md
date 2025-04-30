# Minimax

Minimax is a recursive decision-making algorithm used in two-player turn-based games like chess. It assumes that both players play optimally—one tries to maximize the score (Max), while the other tries to minimize it (Min). The algorithm builds a game tree to a certain depth, evaluates the leaf nodes using a scoring function, and propagates the best values back up the tree to choose the optimal move.

However, basic Minimax evaluates all possible moves, which becomes computationally expensive as the depth increases.

# Alpha-Beta Pruning

Alpha-Beta Pruning is an optimized version of Minimax. It reduces the number of nodes evaluated by pruning branches that cannot possibly affect the final decision. It uses two parameters:

alpha: the best value that the maximizing player can guarantee so far

beta: the best value that the minimizing player can guarantee so far

If a node is found to be worse than a previously examined option, it's skipped entirely. This pruning significantly improves performance, allowing deeper searches within the same time constraints.



# Instructions for running codes

Clone the repository 

```https://github.com/greeshma0906/AI_Algo2.git```

## For Minimax:

Go to the directory

```cd/AI_Algo/Mini_Max``` 

create a virtual environment then activate it using

```venv/Scripts/activate```


Install requirements using

```pip install -r requirements.txt```

Next, run 

```python minimax_chess.py```

## For Alpha-beta pruning:
Go to the directory

```cd/AI_Algo/Alpha-beta-pruning```

 create a virtual environment then activate it using

 ```venv/Scripts/activate```

Install requirements using,

```pip install -r requirements.txt```

Next, run 

```python chess_alpha_beta.py```



If at all you come accross an error stating the environemnt is broken please create a new environment by running the command:

```python -m venv venv```


