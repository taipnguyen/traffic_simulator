import pygame
from enum import Enum

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 
time_passed = 0 
traffic_light_time = 6 

class car():
    def __init__(self, x, next_car = None):
        self.car_pos = pygame.Vector2(x, screen.get_height()/2)
        self.car_size = pygame.Vector2(200,100)
        self.velocity = 100
        self.next_car = next_car
    def get_pos(self):
        return self.car_pos
    def get_velocity(self):
        return self.velocity
    def get_next(self):
        return self.next_car
    def get_size(self):
        return self.car_size
    
class light_color(Enum):
    RED = 1
    GREEN = 2
        
first_car = car(screen.get_width()/2)
stop_pos = pygame.Vector2(1000,300)
initial_velocity = 100

second_car = car(first_car.get_pos().x - 300)
third_car = car(second_car.get_pos().x - 300)

order = [third_car, second_car, first_car]
light = light_color.RED

def stop_before_hitting(dt, car_in_front, car_size, initial_velocity, car_behind, car_behind_velocity):
    three_second_distance = car_behind_velocity * 3
    velocity = car_behind_velocity + (initial_velocity/3) * dt
    if car_behind.x + car_size.x + three_second_distance >= car_in_front.x:
        velocity = car_behind_velocity + (-initial_velocity/3) * dt   
    return velocity

def stop_before_hitting_light(dt, car_in_front, car_size, initial_velocity, car_behind, car_behind_velocity, light):
    three_second_distance = car_behind_velocity * 3
    velocity = car_behind_velocity + (initial_velocity/3) * dt
    if car_behind.x + car_size.x + three_second_distance >= car_in_front.x:
        if light == light_color.RED:
            velocity = car_behind_velocity + (-initial_velocity/3) * dt   
    return velocity

def mover(dt, second_pos, second_velocity):
    if second_velocity > 0:
        second_pos.x = second_pos.x + second_velocity * dt
    return second_pos

def dont_collide(dt, player_pos, car_size, second_pos, second_velocity):
    if second_pos.x + car_size.x >= player_pos.x:
        second_velocity = 0 * dt
    return second_velocity

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("purple")
    
    # Car
    for i in range(len(order)):
        pygame.draw.rect(screen, "black", pygame.Rect(order[i].get_pos(),order[i].get_size()))
        
    if light == light_color.RED:
        pygame.draw.circle(screen, "red", (1000,300), 50)
    elif light == light_color.GREEN:
        pygame.draw.circle(screen, "green", (1000,300), 50)
        
    # Slow down
    # Isn't there like a 3 second rule?
    
    # Make sure not to hit the car in front
    for i in range(len(order)-1):
        def index(i):
            return i % len(order)
        order[i].velocity = stop_before_hitting(dt, order[index(i+1)].get_pos(), order[i].get_size(), initial_velocity, order[index(i)].get_pos(), order[index(i)].get_velocity())
    order[-1].velocity = stop_before_hitting_light(dt, stop_pos, order[-1].get_size(), initial_velocity, order[-1].get_pos(), order[-1].get_velocity(), light)

    
    # Teleport cars to the back
    for i in range(len(order)):
        if order[i].get_pos().x > 1100:
            order[i].car_pos.x = 0
            new_car = order.pop(i)
            order.insert(0,new_car)
    # Mover
    for i in range(len(order)):
        order[i].car_pos = mover(dt, order[i].get_pos(), order[i].get_velocity())
    
    pygame.display.flip()
    if int(time_passed) // traffic_light_time % 2:
        light = light_color.GREEN
    else:
        light = light_color.RED
    time_passed = time_passed + dt
    dt = clock.tick(60) / 1000
    
    
pygame.quit()