import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2
import random 
from car import Car
from background import Background

class Simulation:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Traffic simulation")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False
        
    
    def update_lane(self, car_index):
        
        i = car_index
        car_x, car_y = self.cars[i].position
        ambulance_x, ambulance_y = self.ambulance.position
        police_x, police_y = self.police.position
        speedup_car = False
        if abs(car_y - police_y) < self.lane_error_margin:
            if abs(car_y - self.lanes[1])< self.lane_error_margin and car_x > police_x and car_x - police_x < self.safe_distance:
                self.cars[i].steering = -30
                speedup_car = True
                    
            elif abs(car_y - self.lanes[2]) < self.lane_error_margin and car_x > police_x and car_x - police_x < self.safe_distance:
                self.cars[i].steering = 30
                speedup_car = True
                
            elif abs(car_y - self.lanes[3])< self.lane_error_margin and car_x < police_x and police_x - car_x < self.safe_distance:
                self.cars[i].steering = 30
                speedup_car = True
                
            elif abs(car_y - self.lanes[4])< self.lane_error_margin and car_x < police_x and police_x - car_x < self.safe_distance:
                self.cars[i].steering = -30
                speedup_car = True
            else:
                pass
            
            
            
        if abs(car_y  - ambulance_y) < self.lane_error_margin:
            if abs(car_y - self.lanes[1]) < self.lane_error_margin and car_x > ambulance_x and car_x - ambulance_x < self.safe_distance:
                self.cars[i].steering = -30
                speedup_car = True
                    
            elif abs(car_y - self.lanes[2]) < self.lane_error_margin and car_x > ambulance_x and car_x - ambulance_x < self.safe_distance:
                self.cars[i].steering = 30
                speedup_car = True
            
            elif abs(car_y - self.lanes[3]) < self.lane_error_margin and car_x < ambulance_x and ambulance_x - car_x < self.safe_distance:
                self.cars[i].steering = 30
                speedup_car = True
                    
            elif abs(car_y - self.lanes[4]) < self.lane_error_margin and car_x < ambulance_x and ambulance_x - car_x < self.safe_distance:
                self.cars[i].steering = -30
                speedup_car = True
            else:
                pass    
            
        if speedup_car:
            self.cars[i].max_acceleration = 8.0
            self.cars[i].max_velocity = 8.0            
            self.cars[i].counter = 30
        
    def random_lane_generator(self):
        #generate random lane from 1 to 4:
        return random.randint(1,4)
        
    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        cars_list = ["blueAquaCar.png", "blueCar.png", "greenCar.png", \
                    "orangeCar.png", "pinkCar.png", "redBlueCar.png",\
                    "redWhiteCar.png", "whiteCar.png", "yellowCar.png", "yellowWhiteCar.png"]
        
        car_image_paths = []
        car_images = []
        self.cars = []
        for car_image in cars_list:
            car_image_paths.append(os.path.join(current_dir, "cars/", car_image))
            
        
        for car_image_path in car_image_paths:
            car_images.append(pygame.image.load(car_image_path))
        
        for i in range(len(car_images)):
            car_images[i] = pygame.transform.scale(car_images[i], (33,21))
            
        
        police_image_path = os.path.join(current_dir, "cars/police.png")
        police_image = pygame.image.load(police_image_path)
        police_image = pygame.transform.scale(police_image, (48,35))
        
        ambulance_image_path = os.path.join(current_dir, "cars/ambulance.png")
        ambulance_image = pygame.image.load(ambulance_image_path)
        ambulance_image = pygame.transform.scale(ambulance_image, (42,24))
        
        self.lanes = {1:9, 2:10, 3:11.3, 4:12.4}
        #Initializations at random locations
        #Initiaization of cars: (x, y, angle=0.0, length=4, max_steering=30, max_acceleration=5.0)
        self.cars.append(Car(-58, self.lanes[1]))                #lane-1,  towards right
        self.cars.append(Car(-28, self.lanes[1]))                
        self.cars.append(Car(-18, self.lanes[1]))
        self.cars.append(Car(-6, self.lanes[1]))
        self.cars.append(Car(7, self.lanes[1]))
        self.cars.append(Car(15, self.lanes[1]))
        
        self.cars.append(Car(-49,self.lanes[2]))                 #lane-2, towards right
        self.cars.append(Car(-31,self.lanes[2]))
        self.cars.append(Car(-21,self.lanes[2]))
        self.cars.append(Car(-14,self.lanes[2]))
        #self.cars.append(Car(-7,self.lanes[2]))
        self.cars.append(Car(2,self.lanes[2]))
        #self.cars.append(Car(13,self.lanes[2]))
        self.cars.append(Car(22,self.lanes[2]))
        
        self.cars.append(Car(79,self.lanes[3], 180))          #lane-3, towards left
        self.cars.append(Car(63,self.lanes[3], 180))
        self.cars.append(Car(52,self.lanes[3], 180))
        self.cars.append(Car(40,self.lanes[3], 180))
        #self.cars.append(Car(40,self.lanes[3], 180))
        self.cars.append(Car(32,self.lanes[3], 180))
        self.cars.append(Car(25,self.lanes[3], 180))
        
        self.cars.append(Car(94,self.lanes[4], 180))          #lane-4, towards left
        self.cars.append(Car(87,self.lanes[4], 180))
        #self.cars.append(Car(81,self.lanes[4], 180))
        self.cars.append(Car(71,self.lanes[4], 180))
        self.cars.append(Car(55,self.lanes[4], 180))
        self.cars.append(Car(48,self.lanes[4], 180))
        self.cars.append(Car(27,self.lanes[4], 180))
        
        no_of_cars = len(self.cars)
        
        #initializing ambulance car
        #random_ambulance_lane = self.random_lane_generator()
        random_ambulance_lane = 1
        if random_ambulance_lane == 1:
            random_x = random.randint(-20, -10)
            self.ambulance = Car(random_x, self.lanes[1])
            
        elif random_ambulance_lane == 2:   
            random_x = random.randint(-20, -10)
            self.ambulance = Car(random_x, self.lanes[2])
        
        elif random_ambulance_lane == 3:   
            random_x = random.randint(55, 70)
            self.ambulance = Car(random_x, self.lanes[3], 180)
            
        else:   
            random_x = random.randint(55, 70)
            self.ambulance = Car(random_x, self.lanes[4], 180)
            
        self.ambulance.max_acceleration = 7.0
        self.ambulance.max_velocity = 6.0
        
        #initializing police car
        #random_police_lane = self.random_lane_generator()
        random_police_lane = 2
        if random_police_lane == 1:
            random_x = random.randint(-40, -25)
            self.police = Car(random_x, self.lanes[1])
            
        elif random_police_lane == 2:   
            random_x = random.randint(-40, -25)
            self.police = Car(random_x, self.lanes[2])
        
        elif random_police_lane == 3:   
            random_x = random.randint(70, 90)
            self.police = Car(random_x, self.lanes[3], 180)
            
        else:   
            random_x = random.randint(70, 90)
            self.police = Car(random_x, self.lanes[4], 180)
    
        self.police.max_acceleration = 7.0
        self.police.max_velocity = 6.0
        self.safe_distance = 4.5
        self.lane_error_margin = 0.5    
        ppu = 32
        
        rotated = [None]*no_of_cars
        rect = [None]*no_of_cars
        back = Background('background_image.png', [0,0])
        
        #iterator = 1
        while not self.exit:
            
            dt = self.clock.get_time() / 1000
            # Event queue
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
            
            #if iterator%500==0:
            self.ambulance.acceleration = self.ambulance.brake_deceleration
            #self.ambulance.steering = 0
            self.ambulance.update(dt)
            #ambulance_x, ambulance_y = ambulance.position
                 
            #if (iterator+200)%500==0:
            self.police.acceleration = self.police.brake_deceleration
            #self.police.steering = 0
            self.police.update(dt)
            #police_x , police_y = self.police.position
            #logic
            for i in range(no_of_cars):
                self.cars[i].acceleration = self.cars[i].brake_deceleration
                #self.cars[i].steering = 0
                self.cars[i].update(dt)
                if self.cars[i].counter > 1:
                    self.cars[i].counter -= 1
                    continue
                
                if self.cars[i].counter == 1:
                    self.cars[i].max_acceleration = 4.0
                    self.cars[i].max_velocity = 3.0 
                    self.cars[i].steering = 0
                    print(self.cars[i].angle)
                    if self.cars[i].angle >= -90 and self.cars[i].angle <90:
                        self.cars[i].angle = 0
                    else:
                        self.cars[i].angle = 180
                        
                    self.cars[i].counter -= 1
                #self.cars[i].angle = 0
            
                #car_x, car_y = self.cars[i].position
                
                self.update_lane(i)
                
                
            print(self.police.position)

            
            # Drawing
            #self.screen.fill((0, 0, 0))        #empty background
            self.screen.fill([255, 255, 255])   #roads' background
            self.screen.blit(back.image, back.rect)
            
            for i in range(no_of_cars):
                    
                rotated[i] = pygame.transform.rotate(car_images[i%len(cars_list)], self.cars[i].angle)
                rect[i] = rotated[i].get_rect()
                self.screen.blit(rotated[i], self.cars[i].position * ppu - (rect[i].width / 2, rect[i].height / 2))
                
            #if iterator>=500:
            rotated_ambulance = pygame.transform.rotate(ambulance_image, self.ambulance.angle)
            rect_ambulance = rotated_ambulance.get_rect()
            self.screen.blit(rotated_ambulance, self.ambulance.position * ppu - (rect_ambulance.width / 2, rect_ambulance.height / 2))
                
            #if iterator+200>=500:
            rotated_police = pygame.transform.rotate(police_image, self.police.angle)
            rect_police = rotated_police.get_rect()
            self.screen.blit(rotated_police, self.police.position * ppu - (rect_police.width / 2, rect_police.height / 2))
                
#            rotated[2] = pygame.transform.rotate(car_images[2], self.cars[2].angle)
#            rect[2] = rotated[2].get_rect()
#            self.screen.blit(rotated[2], self.cars[2].position * ppu - (rect[2].width / 2, rect[2].height / 2))
            
            pygame.display.flip()
            #iterator += 1
            #print(iterator)
            self.clock.tick(self.ticks)
        #end of game loop    
            
        pygame.quit()


if __name__ == '__main__':
    game = Simulation()
    game.run()
