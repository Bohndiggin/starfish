import math
G = 6.67384 * 10 ** -11
g_units = "m^3kg^-1s^-2"
speed_of_light = 299792458
AU = 149597870
sb_constant = 5.670374419 * 10 **  -8
k_boiling_point = 373.15
cubic_meter_of_rock_mass = 2515
cubic_meter_of_ice_mass = 919
cubic_meter_of_metal_mass = 8908
solar_mass = 1.98847 * 10 **  30
solar_radius = 695700
solar_luminosity = 3.828 * 10 **  26
solar_temp = 5772
mercury_mass = 3.3011 * 10 **  23
mercury_temp = 340.15
earth_mass = 5.9722 * 10 **  24
earth_radius = 6371
earth_semi_major_axis = 149597887
earth_temp = 288
lunar_mass = 7.342 * 10 **  22
lunar_semi_major_axis = 384399
lunar_temp = 250
jupiter_mass = 1.899 * 10 ** 27
jupiter_semi_major_axis = 5.2038 * AU
jupiter_temp = 165
mars_mass = 6.4171 * 10 ** 23
mars_semi_major_axis = 1.524 * AU
mars_radius = 3396.2
mars_temp = 213.15
unreal_factor = 500
zoom_scale = 0.1
time_period = 0.1

class StarTypes:
    def __init__(self, min_temp, max_temp, class_name, min_mass, max_mass, min_radius, max_radius, min_lumens, max_lumens, frequency) -> None:
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.class_name = class_name
        self.min_mass = min_mass
        self.max_mass = max_mass
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.min_lumens = min_lumens
        self.max_lumens = max_lumens
        self.frequency = frequency
    
    def __repr__(self) -> str:
        return f'It is a {self.class_name}-type star!'

star_type_array = [
    StarTypes(30000, 1000000, 'O', 16, 20, 6.6, 8, 30000, 50000, 0.03),
    StarTypes(10000, 30000, 'B', 2.1, 16, 1.8, 6.6, 30000, 25, 0.25),
    StarTypes(7500, 10000, 'A', 1.4, 2.1, 1.4, 1.8, 5, 25, 0.85),
    StarTypes(6000, 7500, 'F', 1.04, 1.4, 1.15, 1.4, 1.5, 5, 3.85),
    StarTypes(5200, 6000, 'G', 0.8, 1.04, 0.96, 1.15, 0.6, 1.5, 10),
    StarTypes(3700, 5200, 'K', 0.45, 0.8, 0.7, 0.96, 0.08, 0.6, 22.1),
    StarTypes(2400, 3700, 'M', 0.08, 0.45, 0.00001, 0.07, 0.00001, 0.08, 100)
]

class PlanetTypes:
    def __init__(self, min_temperature:int, max_temperature:int, planet_type:str) -> None:
        self.min_temperature = min_temperature
        self.max_temperature = max_temperature
        self.planet_type = planet_type

    def __repr__(self) -> str:
        return f"It's a {self.planet_type}"

temperature_array_rocky = [
    PlanetTypes(0, 50, 'rocky cold'),
    PlanetTypes(50, 100, 'rocky chilly'),
    PlanetTypes(100, 200, 'rocky brisky'),
    PlanetTypes(200, 275, 'rocky frozen'),
    PlanetTypes(275, 300, 'rocky earth-like'),
    PlanetTypes(300, k_boiling_point, 'rocky desert-world'),
    PlanetTypes(k_boiling_point, 450, 'rocky boiling'),
    PlanetTypes(450, 600, 'lava-world'),
    PlanetTypes(600, math.inf, 'hell-world')
]

temperature_array_icy = [
    PlanetTypes(0, 50, 'icy cold'),
    PlanetTypes(50, 100, 'icy chilly'),
    PlanetTypes(100, 200, 'icy brisky'),
    PlanetTypes(200, 275, 'icy frozen'),
    PlanetTypes(275, 300, 'ocean'),
    PlanetTypes(300, k_boiling_point, 'Hot-Ocean')
]

temperature_array_metalic = [
    PlanetTypes(0, 50, 'metalic cold'),
    PlanetTypes(50, 100, 'metalic chilly'),
    PlanetTypes(100, 200, 'metalic brisky'),
    PlanetTypes(200, 275, 'metalic frozen'),
    PlanetTypes(275, 300, 'metalic rust-world'),
    PlanetTypes(300, k_boiling_point, 'pot-world'),
    PlanetTypes(k_boiling_point, 450, 'metalic boiling'),
    PlanetTypes(450, 600, 'stovetop'),
    PlanetTypes(600, 1200, 'oven-world'),
    PlanetTypes(1200, math.inf, 'tartarus')
]

class PositionVector:
    def __init__(self, position_x:float, position_y:float, true_anomaly:math.radians) -> None:
        self.position_x = position_x
        self.position_y = position_y
        self.true_anomaly = true_anomaly

    def set_position(self, position_x:float, position_y:float, true_anomaly:math.radians):
        self.position_x = position_x
        self.position_y = position_y
        self.true_anomaly = true_anomaly

    def calculate_distance(self, other_position):
        displacement_vector = [
            (self.position_x - other_position.position_X),
            (self.position_y - other_position.position_y)
            ]
        distance = math.sqrt(displacement_vector[0]**2 + displacement_vector[1]**2)
        return distance

    def __repr__(self) -> str:
        return f'coordinates: {self.position}, true_anomaly: {self.true_anomaly}'

class VelocityVector:
    def __init__(self, velocity:float, true_anomaly:math.radians) -> None:
        self.velocity = velocity
        self.true_anomaly = true_anomaly

    def set_velocity(self, velocity:float, true_anomaly:math.radians):
        self.velocity = velocity
        self.true_anomaly = true_anomaly

    def __repr__(self) -> str:
        return f'velocity: {self.velocity}, true_anomaly: {self.true_anomaly}'
    
class Km: #TODO make a value / unit class that can be added and junk
    def __init__(self, km:int) -> None:
        self.km = km

    def __repr__(self) -> str:
        return f'{self.km} Km'