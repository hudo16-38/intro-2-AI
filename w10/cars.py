from genetic import *
import numpy as np


class MyCar(Car):
    def __init__(self, chromosome, **kwargs):
        super(MyCar, self).__init__(**kwargs)

        self.input_dim = len(self.sensors) + 2  # two additional inputs for the current speed and the current turn
        self.output_dim = 2  # there are 2 options: 1, go left/right and 2, go forward/backward

        if chromosome is None:
            # # # YOUR CODE GOES HERE # # #
            #8 hidden neurons
            self.chromosome = list(np.random.normal(size=(8*(self.input_dim+1))+(self.output_dim*9),scale=1))
        else:
            self.chromosome = chromosome

        self.W_in = np.array(self.chromosome[:8*(self.input_dim+1)]).reshape(8, self.input_dim+1)
        #print("W_in is ok")

        self.W_out = np.array(self.chromosome[8*(self.input_dim+1):]).reshape(self.output_dim, 9)
        #print("W_out is ok")

    def compute_output(self):
        sensor_norms = []
        # create an array of sensor lengths. Afterwards, append to this array the speed and the turn of the car
        # (self.speed and self.turn). This array serves as an input to the network (but do not forget the bias)
        # the sensor lengths values are originally quite large - are in the interval <0, 200>. To prevent "explosion" in
        # the neural network, normalize the lengths to smaller interval, e.g. <0, 10>

        for end1, end2 in self.sensors:
            x1,y1 = end1
            x2, y2 = end2
            dx = x2 - x1
            dy = y2 - y1
            norm = np.sqrt(dx**2 + dy**2) #norm of sensor
            sensor_norms.append(norm/20) 
        
        sensor_norms.extend([self.speed, self.turn, 1])
        sensor_norms = np.array(sensor_norms)


        # # # YOUR CODE GOES HERE # # #
        # use the input (inp) to calculate the instructions for the car at the given state
        # do not forget to add bias neuron before each projection!
        # for adding bias you can use np.concatenate(( state , [1]))
        # between two layers use an activation function. sigmoid(x) is already implemented, however, feel free to use
        # other, meaningful activation function
        # at the end of the network, use hyperbolic tangent -> to ensure that the change is in the range (-1, 1)

        hidden_output = np.concatenate((sigmoid(self.W_in@sensor_norms), [1])) #add bias
        #print(f"{hidden_output=}")
        output = np.tanh(self.W_out@hidden_output)
    
        return output

    def update_parameters(self, instructions):
        # # # YOUR CODE GOES HERE # # #
        # use the values outputted from the neural network (instructions) to change the speed and turn of the car
        o1, o2 = instructions
        self.speed += o1 * self.max_speed_change
        self.turn += o2 * self.max_turn_change

        self.speed = np.clip(self.speed, self.speed_limit[0], self.speed_limit[1])
        self.turn = np.clip(self.turn, self.turn_limit[0], self.turn_limit[1])
        self.orientation += self.turn


class MyRaceCars(RaceCars):
    def __init__(self, *args, **kwargs):
        super(MyRaceCars, self).__init__(*args, **kwargs)

    def generate_individual(self, chromosome=None):
        initial_position = [500, 600 + random.randint(-25, 25)]
        orientation = 90
        new_car = MyCar(chromosome, position=initial_position, orientation=orientation,
                        additional_scale=self.scale_factor)
        sensors = []
        if self.show_sens:
            for _ in new_car.sensors:
                sensors.append(self.canvas.create_line(0, 0, 0, 0, dash=(2, 1)))
        return [new_car, self.canvas.create_image(initial_position), sensors]


if __name__ == '__main__':
    track = create_track()

    # useful parameters to play with:
    population_size = 16        # total population size used for training
    select_top = 4              # during selection, only the best select_top cars are chosen as parents

    show_training = True        # each generation is shown on canvas
    show_all_cars = False       # the code is faster if not all cars are always displayed
    displayed_cars = 8         # only the first few cars are displayed

    # show_training = False     # the training is done in the background
    show_every_n = 3            # the best cars are shown after every few generations (due to faster training)

    mutation_prob = 0.05        # mutation probability for number mutation
    deviation = 1               # this standard deviation used when mutating a chromosome

    RC = MyRaceCars(track, population_size=population_size, show_sensors=False, gen_steps=1000, n_gens=100,
                    show_all_cars=show_all_cars, select_top=select_top, mutation_prob=mutation_prob,
                    show_training=show_training, displayed_cars=displayed_cars, vis_pause=10, show_every_n=show_every_n,
                    can_width=1100, deviation=deviation)

    RC.run_simulation()
    
