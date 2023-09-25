from __future__ import annotations
from typing import List, Tuple
from chromosome import Chromosome
from genetic_algorithm import GeneticAlgorithm
from random import random, randrange
from copy import deepcopy


class SimpleEquation(Chromosome):

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y

    def fitness(self) -> float:  # 6x - x^2 + 4y - y^2
        return 6 * self.x - self.x * self.y + 4 * self.y - self.y * self.y

    @classmethod
    def random_instance(cls) -> SimpleEquation:
        return SimpleEquation(randrange(100), randrange(100))

    def crossover(self, other: SimpleEquation) -> Tuple[SimpleEquation, SimpleEquation]:
        child1: SimpleEquation = deepcopy(self)
        child2: SimpleEquation = deepcopy(other)

        child1.y = other.y
        child2.y = self.y

        return child1, child2

    def mutate(self) -> None:
        if random() > 0.5:
            self._mutate_x()
        else:
            self._mutate_y()

    def _mutate_x(self) -> None:
        if random() > 0.5:
            self.x += 1
        else:
            self.x -= 1

    def _mutate_y(self) -> None:
        if random() > 0.5:
            self.y += 1
        else:
            self.y -= 1

    def __str__(self) -> str:
        return f'X: {self.x}, Y: {self.y}, Fitness: {self.fitness()}'


if __name__ == '__main__':
    initial_population: List[SimpleEquation] = [SimpleEquation.random_instance() for _ in range(20)]
    gen_alg: GeneticAlgorithm[SimpleEquation] = GeneticAlgorithm(
        initial_population=initial_population,
        threshold=23.0,
        max_generations=100,
        mutation_chance=0.1,
        crossover_chance=0.7,
    )
    result = gen_alg.run()
    print(result)




