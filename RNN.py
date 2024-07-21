from class_for_RNN import Drone2DSimulator
import pygame
import numpy as np

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("2D Drone Simulation for RNN's or Other Applications")
    #size of each generated sequence of control inputs, outputs frmo RNN
    ss = 5
    completed_task = False
    #Create Simulation
    sim = Drone2DSimulator()

    result = sim.get_feedback()
    print(result)
    #Perform Reinforcement learning to generate array of controls
    #Here an example randomly generated, replace for loops with generating RNN outputs:
    RNN_output = np.array([(0, 0)]) #initial array


    #randomly generate first control sequence array:
    for _ in range(ss):
        random_tuple0 = (np.random.randint(0, 2), np.random.randint(0, 2))
        RNN_output = np.vstack((RNN_output, random_tuple0))

    sim.run(RNN_output[:ss])  #Run first generated sequence

    #further control sequences, generated dynamically, lively:
    sequence = 0
    while not completed_task:
        sequence += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            break






        #randomly generate next control sequence array
        # #ACTUALLY REPLACE THIS CODE SNIPEET WITH THE CALCULATION OF THE NEXT CONTROL SEQUENCE FROM THE NEURAL NETWORK BASED ON THE RESULT, INSTEAD OF RANDOMLY GENERATING IT:
        for _ in range(ss):
            random_tuple1 = (np.random.randint(0, 2), np.random.randint(0, 2))
            RNN_output = np.vstack((RNN_output, random_tuple1))
            






        sim.run(RNN_output[sequence*ss:])  # Run next sequence

        result = sim.get_feedback()
        print(result)

    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()
