import pygame, neat
from game import Car

def run_cars(genomes, config):
    nets, cars = [], []

    for _, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car())

    pygame.init()
    map = pygame.image.load('assets/new_map.png')
    screen = pygame.display.set_mode((map.get_width(), map.get_height()))
    font = pygame.font.SysFont("Arial", 30)

    global generation
    generation += 1
    while True:
        screen.blit(map, (0, 0))
        screen.blit(font.render(f"Generation {generation}", True, (255, 0, 255)), (0, 0))

        # Input data and get result from neural network
        for index, car in enumerate(cars):
            output = nets[index].activate(car.get_inputs())
            i = output.index(max(output))
            if i == 0:
                car.angle += 10
            elif i == 1:
                car.angle += -10
            elif i == 2:
                pass

        # Reward car and update it
        remaining_cars = 0
        for i, car in enumerate(cars):
            if car.is_alive:
                remaining_cars += 1
                car.update(map)
                genomes[i][1].fitness += car.get_reward()
                car.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        if remaining_cars == 0:
            break

        screen.blit(font.render(f"Cars: {remaining_cars}", True, (255, 0, 0)), (0, 30))
        pygame.display.flip()


generation = 0
config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, "./config.txt")
neat.Population(config).run(run_cars, 1000)
