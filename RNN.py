from class_for_RNN import Drone2DSimulator
import pygame
import numpy as np

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("2D Drone Simulation for RNN's or Other Applications")
    #size of each generated sequence of control inputs, outputs frmo RNN
    ss = 5
    #Create Simulation
    sim = Drone2DSimulator()
    #Perform Reinforcement learning to generate array of controls
    #Here an example randomly generated, replace for loops with generating RNN outputs:
    RNN_output = np.array([(0, 0)]) #initial array


    #randomly generate first control sequence array:
    for _ in range(ss):
        random_tuple0 = (np.random.randint(0, 2), np.random.randint(0, 2))
        RNN_output = np.vstack((RNN_output, random_tuple0))

    sim.run(RNN_output[:ss])  #Run first generated sequence

    for sequence in range(2000): #for example 2000 more generations of ss controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            break

        #randomly generate next control sequence array:
        for _ in range(ss):
            random_tuple1 = (np.random.randint(0, 2), np.random.randint(0, 2))
            RNN_output = np.vstack((RNN_output, random_tuple1))
            
        sim.run(RNN_output[(sequence+1)*ss:])  # Run next sequence


    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()