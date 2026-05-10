import random
from typing import List

import numpy as np

from Birb import Birb
from CONSTANTS import GENETIC_CROSSOVER_SWAP_RATE, INCREASED_GENETIC_MUTATION_RATE, DEFAULT_GENETIC_MUTATION_RATE


def crossover(birb1: Birb, birb2: Birb) -> Birb:
    # if swapping both weights and biases, then maybe we end up with NNs that look like copies of each other.
    # If we swap only biases then maybe it is a "looser" influence.
    offspring = Birb()
    offspring.generation = birb1.generation + 1
    offspring.rgb = (
        random.randint(birb1.rgb[0], birb2.rgb[0]) if birb2.rgb[0] >= birb1.rgb[0] else random.randint(birb2.rgb[0], birb1.rgb[0]),
        random.randint(birb1.rgb[1], birb2.rgb[1]) if birb2.rgb[1] >= birb1.rgb[1] else random.randint(birb2.rgb[1], birb1.rgb[1]),
        random.randint(birb1.rgb[2], birb2.rgb[2]) if birb2.rgb[2] >= birb1.rgb[2] else random.randint(birb2.rgb[2], birb1.rgb[2]),
    )
    crossover_swap_choice = random.choice((True, False))  # True = b1, w1; False = b2, w2

    # masked swappings
    for layer_idx in range(len(birb1.brain.weights)):
        w1 = birb1.brain.weights[layer_idx].flatten()
        w2 = birb2.brain.weights[layer_idx].flatten()
        shape = birb1.brain.weights[layer_idx].shape

        # for i in range(len(w1)):  # don't swap weights
        #     if random.random() < GENETIC_CROSSOVER_SWAP_RATE:
        #         w1[i], w2[i] = w2[i], w1[i]

        if crossover_swap_choice:
            offspring.brain.weights[layer_idx] = np.array(w1).reshape(shape)
        else:
            offspring.brain.weights[layer_idx] = np.array(w2).reshape(shape)

    # bias and weight don't match to same neurons. too much chaos maybe
    for layer_idx in range(len(birb1.brain.biases)):
        b1 = list(birb1.brain.biases[layer_idx].flatten())
        b2 = list(birb2.brain.biases[layer_idx].flatten())
        shape = birb1.brain.biases[layer_idx].shape

        for i in range(len(b1)):
            if random.random() < GENETIC_CROSSOVER_SWAP_RATE:
                b1[i], b2[i] = b2[i], b1[i]

        if crossover_swap_choice:
            offspring.brain.biases[layer_idx] = np.array(b1).reshape(shape)
        else:
            offspring.brain.biases[layer_idx] = np.array(b2).reshape(shape)

    return offspring


def mutate(gene: np.ndarray) -> np.ndarray:
    return gene + gene * np.random.normal(size=gene.shape)


def get_next_gen_birbs(birbs: List[Birb], max_score: int) -> List[Birb]:
    # select top
    birbs = sorted(birbs, key=lambda x: x.fitness, reverse=True)  # desc order

    # crossover/breed
    selection = birbs[:4]
    next_birbs = selection  # continue top 4, aka Selection

    # 1 crossover of top 2
    next_birbs.append(crossover(birbs[0], birbs[1]))

    # 3 crossover of random 2
    next_birbs.append(crossover(random.choice(selection), random.choice(selection)))
    next_birbs.append(crossover(random.choice(selection), random.choice(selection)))
    next_birbs.append(crossover(random.choice(selection), random.choice(selection)))

    # 2 direct of top 4
    next_birbs.append(random.choice(selection))
    next_birbs.append(random.choice(selection))

    # mutate
    mutation_rate = INCREASED_GENETIC_MUTATION_RATE if max_score == 0 else DEFAULT_GENETIC_MUTATION_RATE

    for birb in next_birbs:
        for idx, layer in enumerate(birb.brain.weights):
            mutated_weights = mutate(layer)
            mask = np.random.random(size=layer.shape) < mutation_rate
            birb.brain.weights[idx] = np.where(mask, mutated_weights, layer)

        for idx, layer in enumerate(birb.brain.biases):
            mutated_biases = mutate(layer)
            mask = np.random.random(size=layer.shape) < mutation_rate
            birb.brain.biases[idx] = np.where(mask, mutated_biases, layer)

    return next_birbs

# a = [Birb() for i in range(10)]
# for i in a:
#     print(vars(i.brain))
#
# b = get_next_gen_birbs(a)
# print()
#
# # b = [Birb(), Birb()]
# for i in b:
#     print(vars(i.brain))

# a = Birb()
# b = Birb()
# print(vars(a.brain), vars(b.brain), sep="\n")
# x1 = crossover(a, b)
#
# print(vars(x1.brain), sep="\n")
