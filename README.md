# HideOrJump
A Game Environnement for Reinforcement Learning 
1. Play all agents
2. Rank them in descending order of score
3. Make them evolve
4. We stop learning if we've exceeded the maximum number of generations we've set ourselves, or if we've reached our target score. 

Neural networks are simply composed of two hidden layers, each of size 24. To evolve a neural network, we randomly change a fixed number of weights. 

The evolution is performed as follows:
1. For the first 25% agents, nothing is changed 
2. For the next 25%, 2% of the neural network's weights are mutated.
3. For the next 25%, we mutate 4% of the neural network weights.
4. For the next 25%, we mutate 9% of the neural network weights.

You can change these parameters in the 'GeneticAgentParameters' class.

To be able to compare each agent effectively, we make them all play on the same world, every generation. This limits bias, such as an agent constantly bending down, who might get a good score if the first obstacles are all high. In fact, to speed up learning, we have carried out all training on a single world. If an agent achieves the target score, we then test it on other worlds to check that our agent is working properly and hasn't just learned the training world "by heart". To avoid this, we could also have cumulated the rewards between the different worlds with a gamma learning rate.

The number of generations required for our algorithm to work is highly variable, but it generally takes less than 80 generations. The result is very positive. You can record the gameplay of an agent by modifying the RENDER_GAMEPLAY parameter of GeneticAgentParameters. Here's a gif of an agent that beat the game:

[Genetic Algorithm Player](git_results/output.gif)