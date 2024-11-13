import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0 
time_passed = 0 

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
car_size = pygame.Vector2(200,100)
stop_pos = pygame.Vector2(1000,300)
initial_velocity = 100
player_velocity = 100

second_pos = pygame.Vector2(player_pos.x - 300, player_pos.y)
second_velocity = 100

third_pos = pygame.Vector2(second_pos.x - 300, second_pos.y)
third_velocity = 100

def stop_before_hitting(dt, player_pos, car_size, initial_velocity, second_pos, second_velocity):
    second_three_second_distance = second_velocity * 3
    if second_pos.x + car_size.x + second_three_second_distance >= player_pos.x:
        second_velocity = second_velocity + (-initial_velocity/3) * dt 
    else:
        second_velocity = second_velocity + (initial_velocity/3) * dt
    return second_velocity

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
        
    order = [third_pos, second_pos, player_pos]
    order_vel = [third_velocity, second_velocity, player_velocity]
    # Car
    pygame.draw.rect(screen, "black", pygame.Rect(player_pos,car_size))
    
    # Second car
    pygame.draw.rect(screen, "black", pygame.Rect(second_pos, car_size))
    
    #Third car 
    pygame.draw.rect(screen, "black", pygame.Rect(third_pos, car_size))
    # Slow down
    # Isn't there like a 3 second rule?
    
    # Make sure not to hit the car in front
    for i in range(len(order)-1):
        def index(i):
            return i % len(order)
        order_vel[index(i)] = stop_before_hitting(dt, order[index(i+1)], car_size, initial_velocity, order[index(i)], order_vel[index(i)])
    if time_passed < 3:
        order_vel[len(order)-1] = stop_before_hitting(dt, stop_pos, car_size, initial_velocity, order[len(order)-1], order_vel[len(order)-1])

    # Stop at car
    order_vel[1] = dont_collide(dt, player_pos, car_size, second_pos, order_vel[1])
    order_vel[0] = dont_collide(dt, second_pos, car_size, third_pos, order_vel[0])
    
    if player_pos.x > 1100:
        player_pos.x = 0 
    if second_pos.x > 1100:
        second_pos.x = 0 
    if third_pos.x > 1100:
        third_pos.x = 0 
    # Mover
    if order_vel[2] > 0:
        player_pos.x = player_pos.x + order_vel[2] * dt
    second_pos = mover(dt, second_pos, order_vel[1])
    third_pos = mover(dt, third_pos, order_vel[0])
    
    
    # Traffic Light
    if time_passed < 3:
        pygame.draw.circle(screen, "red", stop_pos,50)
    else:
        pygame.draw.circle(screen, "green", stop_pos,50)
    pygame.display.flip()

    time_passed = time_passed + dt
    dt = clock.tick(60) / 1000
    
    
pygame.quit()