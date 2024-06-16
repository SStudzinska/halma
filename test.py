from halma import Halma,random_heuristic, minimax, manhattan_distance_heuristic, player_strategy, chebyshev_distance_heuristic, diff_euclidean_heuristic, \
distance_proximity_heuristic, forward_movement_heuristic, minimax_pruning

halma = Halma()


#halma.play(player_strategy, player_strategy, sum_distance_heuristic, random_heuristic)
#halma.play(minimax_heuristic, player_strategy, diff_euclidean_heuristic, chebyshev_distance_heuristic)
#halma.play(player_strategy, player_strategy, diff_euclidean_heuristic, forward_movement_heuristic)
halma.play(minimax_pruning, player_strategy, forward_movement_heuristic, forward_movement_heuristic)