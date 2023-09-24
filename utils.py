import random
import pygame
from variables import *
import math
import numpy as np


class Star:
    def __init__(self, screen, temperature:int=0, mass:int=0) -> None:
        if temperature:
            self.temperature = temperature
            self.mass = mass
        else:
            star_class_percentage = random.uniform(1, 10000)/100
            for i in star_type_array:
                if star_class_percentage <= i.frequency:
                    self.temperature = random.uniform(i.min_temp, i.max_temp)
                    self.mass = random.uniform(i.min_mass, i.max_mass)
                    break
        self.radius = self.mass ** 0.8 #doesn't seem right... Hmm
        self.km_radius = self.radius * solar_radius
        self.kg_mass = self.mass * solar_mass
        self.luminosity = self.temperature/solar_temp
        self.habitable_zone = self.calculate_habitable_zone()
        self.min_placement_distance = (0.005 * AU) * (self.temperature / solar_temp)
        self.max_placement_distance = (7 * AU) * (self.temperature / solar_temp)
        self.screen = screen
        self.x_location = pygame.display.get_desktop_sizes()[0][0]/2
        self.y_location = pygame.display.get_desktop_sizes()[0][1]/2
        self.position = pygame.Vector2(self.x_location, self.y_location)
        pygame.draw.circle(self.screen, "red", self.position, 40*zoom_scale)

    def calculate_habitable_zone(self):
        far = 1 / ((175 / self.temperature / 0.7 ** (1/4)) ** 2) * 2 / self.radius
        near = 1 / ((300 / self.temperature / 0.7 ** (1/4)) ** 2) * 2 / self.radius
        return [near, far]
    
    def draw(self):
        pygame.draw.circle(self.screen, "orange", self.position, 25)

class Planet:
    def __init__(self, screen, star_orbiting:Star) -> None:
        self.star_orbiting = star_orbiting
        self.eccentricity = (random.betavariate(2, 5) * 0.999)#random.uniform(0.001, 0.999)
        self.radius = random.uniform(600, 9999) # placeholder???
        self.composition = self.calculate_body_composition()
        self.mass = self.calculate_body_mass()
        self.earth_masses = self.mass / earth_mass
        self.sgp = make_sgp(self.mass, self.star_orbiting.mass)
        self.semi_major_axis = random.uniform(self.star_orbiting.min_placement_distance, self.star_orbiting.max_placement_distance)
        self.semi_minor_axis = self.semi_major_axis * math.sqrt(1 - self.eccentricity**2)
        self.velocity = (math.sqrt(self.sgp/self.semi_major_axis) * 1000) / 3.154 * 10 **7
        self.angular_momentum = self.mass * self.velocity * self.semi_major_axis
        self.specific_angular_momentum = self.angular_momentum / self.mass
        self.orbital_period = 2 * math.pi * math.sqrt(self.semi_major_axis**3 / self.sgp)
        # self.average_temperature = self.temperature_get(self.semi_major_axis)
        self.atmosphere = random.uniform(0, 5) # TODO make real
        self.average_temperature = self.temperature_get(self.semi_major_axis)
        self.body_type = self.calculate_body_type()
        self.parameter = self.specific_angular_momentum ** 2 / self.sgp
        self.periapsis = self.semi_major_axis * (1-self.eccentricity)
        self.apoapsis = self.semi_major_axis * (1+self.eccentricity)
        self.max_temperature = self.temperature_get(self.apoapsis) + 37 * self.atmosphere
        self.calculate_ice_blast()
        self.f = self.semi_major_axis * self.eccentricity
        self.argument_of_perigee = random.uniform(0, 360) * math.pi / 180
        self.gravity_relative_to_earth = (self.mass/earth_mass) / (self.radius / earth_radius) ** 2
        self.mean_anomaly = math.radians(random.randint(0, 360))# - self.eccentricity * math.sin(math.radians(0))
        self.current_distance = self.semi_major_axis
        self.offset = [pygame.display.get_desktop_sizes()[0][0]/2, pygame.display.get_desktop_sizes()[0][1]/2]
        self.x_location = pygame.display.get_desktop_sizes()[0][0]/2
        self.y_location = pygame.display.get_desktop_sizes()[0][1]/2
        self.position = pygame.Vector2(self.offset[0], self.offset[1])
        self.screen = screen
        self.orbit_length = self.orbital_period * self.velocity
        self.eccentric_anomaly = self.get_eccentric_anomaly()
        self.true_anomaly = math.radians(0)
        self.color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.draw_size = 40*zoom_scale*(self.radius/earth_radius)
        self.position_vector = PositionVector(0, 0, self.true_anomaly)
        self.velocity_vector = VelocityVector(self.current_speed, self.true_anomaly)
        self.sphere_of_influence = float


    def temperature_get(self, distance):
        return (self.star_orbiting.temperature * math.sqrt(self.star_orbiting.radius/(2*distance)) * 0.7 ** 0.25) + 37 * self.atmosphere

    def update_temperature(self):
        self.current_temperature = self.temperature_get(self.current_distance)

    def calculate_body_composition(self):
        ice_non_normal = random.uniform(1, 100)
        rock_non_normal = random.uniform(1, 100)
        metal_non_normal = random.uniform(1, 100)
        total = ice_non_normal + rock_non_normal + metal_non_normal
        composition = {
            'ice': (ice_non_normal / total) * 100,
            'rock': (rock_non_normal / total) * 100,
            'metal': (metal_non_normal / total) * 100
        }
        return composition

    def calculate_body_mass(self): # in Kg
        self.volume = (4/3) * math.pi * self.radius * self.radius ** 3
        ice_mass = self.volume * (self.composition['ice'] / 100) * cubic_meter_of_ice_mass * 1000 ** 3
        rock_mass = self.volume * (self.composition['rock'] / 100) * cubic_meter_of_rock_mass * 1000 ** 3
        metal_mass = self.volume * (self.composition['metal'] / 100) * cubic_meter_of_metal_mass * 1000 ** 3
        return ice_mass + rock_mass + metal_mass

    def calculate_body_type(self) -> PlanetTypes:
        if self.composition['ice'] > self.composition['rock'] and self.composition['ice'] > self.composition['metal']:
            for i in temperature_array_icy:
                if self.average_temperature > i.min_temperature and self.average_temperature < i.max_temperature:
                    return i
        if self.composition['rock'] > self.composition['ice'] and self.composition['rock'] > self.composition['metal']:
            for i in temperature_array_rocky:
                if self.average_temperature > i.min_temperature and self.average_temperature < i.max_temperature:
                    return i
        if self.composition['metal'] > self.composition['rock'] and self.composition['metal'] > self.composition['ice']:
            for i in temperature_array_metalic:
                if self.average_temperature > i.min_temperature and self.average_temperature < i.max_temperature:
                    return i
    
    def calculate_ice_blast(self):
        if self.max_temperature > k_boiling_point:
            self.radius = self.radius - self.radius * (self.composition['ice'])
            self.composition['ice'] = 0
            self.composition['rock'] = self.composition['rock'] / (self.composition['rock'] + self.composition['metal']) * 100
            self.composition['metal'] = self.composition['metal'] / (self.composition['rock'] + self.composition['metal']) * 100
            self.mass = self.calculate_body_mass()
            self.body_type = self.calculate_body_type()

    def update_location(self):
        self.eccentric_anomaly = self.get_eccentric_anomaly()
        self.big_b = self.eccentricity / (1 + math.sqrt(1 - self.eccentricity ** 2))
        self.true_anomaly = self.eccentric_anomaly + 2*math.atan((self.big_b*math.sin(self.eccentric_anomaly)) / (1-self.big_b*math.cos(self.eccentric_anomaly)))
        self.current_distance = (self.semi_major_axis * (1 - self.eccentricity**2)) / (1+self.eccentricity * math.cos(self.true_anomaly))
        self.current_speed = ((math.sqrt(self.sgp * ((2/self.current_distance)-(1/self.semi_major_axis)))))
        # self.true_anomaly = 2 * math.atan(math.sqrt(1+self.eccentricity/1-self.eccentricity) * math.tan(self.eccentric_anomaly/2))
        self.mean_anomaly += (self.current_speed / self.orbit_length) * unreal_factor * 10 * AU
        self.x_location_perifocal = self.current_distance * math.cos(self.true_anomaly)
        self.y_location_perifocal = self.current_distance * math.sin(self.true_anomaly)
        self.x_location = self.x_location_perifocal * math.cos(self.argument_of_perigee) - self.y_location_perifocal * math.sin(self.argument_of_perigee) #* unreal_factor * AU
        self.y_location = self.x_location_perifocal * math.sin(self.argument_of_perigee) + self.y_location_perifocal * math.cos(self.argument_of_perigee) #* unreal_factor * AU
        self.y_location = (self.y_location / AU * unreal_factor) * zoom_scale + self.offset[1]
        self.x_location = (self.x_location / AU * unreal_factor) * zoom_scale + self.offset[0]
        self.position_vector.set_position(self.x_location, self.y_location, self.true_anomaly)
        self.velocity_vector.set_velocity(self.current_speed, self.true_anomaly)
        self.position.x = self.x_location
        self.position.y = self.y_location
        pygame.draw.circle(self.screen, self.color, self.position, self.draw_size)
        # print(self.x_location)
        # print(self.y_location)
        # print(self.current_speed)
        # print(self.true_anomaly)
        self.update_temperature()

    def get_eccentric_anomaly(self):
        E = self.mean_anomaly
        # while True:
        #     dE = (E - self.eccentricity * math.sin(E) - self.mean_anomaly) / (1 - self.eccentricity * math.cos(E))
        #     E -= dE
        #     if abs(dE) < 1e-6:
        #         return E
        while True:
            dE = (E - self.eccentricity * math.sin(E) - self.mean_anomaly) / (1 - self.eccentricity * math.cos(E))
            E -= dE
            if abs(dE) < 1e-6:
                return E

        # for i in range(10000):
        #     E = self.mean_anomaly + self.eccentricity * math.sin(E)
        # return E
    def two_body_check(self, planet_list:list): # we'll want to give each body a radius of significant influence so we can know if we should run calculations or not
        for i in planet_list:
            distance = self.distance_to_other_body(i)
            if distance < i.sphere_of_influence or distance < self.sphere_of_influence:
                self.two_body_calculation(self, i)

    def distance_to_other_body(self, other_planet):
        distance = self.position_vector.calculate_distance(other_planet.position_vector)
        return distance

    def two_body_calculation(self, other_planet): 
        pass

def make_sgp(mass1, mass2) -> float:
    return G * (mass1 + mass2)
