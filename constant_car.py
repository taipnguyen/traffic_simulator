import pygame 

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 

class car():
    def __init__(self, x, next_car = None):
        self.car_pos = pygame.Vector2(x, screen.get_height()/2)
        self.car_size = pygame.Vector2(200,100)
        self.next_car = next_car
        
first_car = car(screen.get_width()/2)
cars = [first_car]
i = 0 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("purple")

    for i in range(len(cars)):
        pygame.draw.rect(screen, "red", pygame.Rect(cars[i].car_pos,cars[i].car_size))
        cars[i].car_pos.x = cars[i].car_pos.x + 100 * dt

    pygame.display.flip()

    dt = clock.tick(60) / 1000
    
    
pygame.quit()