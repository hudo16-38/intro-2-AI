from cars import *
from utils import *
from genetic import *
import numpy as np

SigmoidCar = MyCar;

class HyperbolicCar(MyCar):
    def __init__(self, chromosome, **kwargs):
        super().__init__(chromosome, **kwargs)
        self.W_3 = np.random.normal(size=(8, 9))
        
    def compute_output(self):
        sensor_norms = []

        for end1, end2 in self.sensors:
            x1,y1 = end1
            x2, y2 = end2
            dx = x2 - x1
            dy = y2 - y1
            norm = np.sqrt(dx**2 + dy**2) 
            sensor_norms.append(norm/20) 
        
        sensor_norms.extend([self.speed, self.turn, 1])
        sensor_norms = np.array(sensor_norms)

        first_output = np.concatenate((np.tanh(self.W_in@sensor_norms), [1])) #9
        second_output = np.concatenate((np.tanh(self.W_3@first_output), [1]))
        output = np.tanh(self.W_out@second_output)
    
        return output

class SigmoidCar(MyCar):
    def __init__(self, chromosome, **kwargs):
        super().__init__(chromosome, **kwargs)
        self.W_3 = np.random.normal(size=(8, 9))
        
    def compute_output(self):
        sensor_norms = []

        for end1, end2 in self.sensors:
            x1,y1 = end1
            x2, y2 = end2
            dx = x2 - x1
            dy = y2 - y1
            norm = np.sqrt(dx**2 + dy**2) 
            sensor_norms.append(norm/20) 
        
        sensor_norms.extend([self.speed, self.turn, 1])
        sensor_norms = np.array(sensor_norms)

        first_output = np.concatenate((sigmoid(self.W_in@sensor_norms), [1])) #9
        second_output = np.concatenate((sigmoid(self.W_3@first_output), [1]))
        output = np.tanh(self.W_out@second_output)
    
        return output



class HyperbolicRaceCars(RaceCars):
    def __init__(self, *args,hyperbolic=True ,**kwargs):
        super(HyperbolicRaceCars, self).__init__(*args, **kwargs)
        
    def generate_individual(self, chromosome=None):
        initial_position = [500, 600 + random.randint(-25, 25)]
        orientation = 90
 
        new_car = HyperbolicCar(chromosome, position=initial_position, orientation=orientation,
                            additional_scale=self.scale_factor)

        sensors = []
        if self.show_sens:
            for _ in new_car.sensors:
                sensors.append(self.canvas.create_line(0, 0, 0, 0, dash=(2, 1)))
        return [new_car, self.canvas.create_image(initial_position), sensors]

class SigmoidRaceCars(RaceCars):
    def __init__(self, *args,hyperbolic=True ,**kwargs):
        super(SigmoidRaceCars, self).__init__(*args, **kwargs)
        
    def generate_individual(self, chromosome=None):
        initial_position = [500, 600 + random.randint(-25, 25)]
        orientation = 90
 
        new_car = SigmoidCar(chromosome, position=initial_position, orientation=orientation,
                            additional_scale=self.scale_factor)

        sensors = []
        if self.show_sens:
            for _ in new_car.sensors:
                sensors.append(self.canvas.create_line(0, 0, 0, 0, dash=(2, 1)))
        return [new_car, self.canvas.create_image(initial_position), sensors]

if __name__ == '__main__':
    track = create_track()

    population_size = 16       
    select_top = 4              

    show_training = True        
    show_all_cars = False       
    displayed_cars = 8         

    # show_training = False   
    show_every_n = 3           

    mutation_prob = 0.7    
    deviation = 1
    n_gens = 50
    gen_steps = 650
    hyp = False

    if hyp:             
        RC = HyperbolicRaceCars(track, population_size=population_size, show_sensors=False, gen_steps=gen_steps, n_gens=n_gens,
                        show_all_cars=show_all_cars, select_top=select_top, mutation_prob=mutation_prob,
                        show_training=show_training, displayed_cars=displayed_cars, vis_pause=10, show_every_n=show_every_n,
                        can_width=1100, deviation=deviation)
    else:
        RC = SigmoidRaceCars(track, population_size=population_size, show_sensors=False, gen_steps=gen_steps, n_gens=n_gens,
                        show_all_cars=show_all_cars, select_top=select_top, mutation_prob=mutation_prob,
                        show_training=show_training, displayed_cars=displayed_cars, vis_pause=10, show_every_n=show_every_n,
                        can_width=1100, deviation=deviation)

    RC.run_simulation()

