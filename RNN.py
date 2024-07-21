from class_for_RNN import Drone2DSimulator
import pygame
import numpy as np

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("2D Drone Simulation for RNN's or Other Applications")
    ss = 5 #size of each generated sequence of control inputs, outputs from RNN
    completed_task = False
    place_tar = True

    #Create Simulation
    sim = Drone2DSimulator()
    target_coo = (np.random.randint(50, sim.WIDTH-50), np.random.randint(50, sim.HEIGHT-50))
    result = sim.get_feedback()
    print(result)

    #Perform Reinforcement learning to generate array of controls
    #Here an example randomly generated, replace for loops with generating RNN outputs:
    RNN_output = np.array([(0, 0)]) #initial array


    #randomly generate first control sequence array:
    for _ in range(ss):
        random_tuple0 = (np.random.randint(0, 2), np.random.randint(0, 2))
        RNN_output = np.vstack((RNN_output, random_tuple0))

    sim.run(RNN_output[:ss], target_coo, place_tar)  #Run first generated sequence

    #further control sequences, generated dynamically, lively:
    sequence = 0

    while not completed_task:
        sequence += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            break





        #randomly generate next control sequence array
        #ACTUALLY REPLACE THIS CODE SNIPEET WITH THE CALCULATION OF THE NEXT CONTROL SEQUENCE FROM THE NEURAL NETWORK BASED ON THE RESULT, INSTEAD OF RANDOMLY GENERATING IT:
        for _ in range(ss):
            random_tuple1 = (np.random.randint(0, 2), np.random.randint(0, 2))
            RNN_output = np.vstack((RNN_output, random_tuple1))
            




        sim.run(RNN_output[sequence*ss:], target_coo, place_tar)  # Run next sequence

        result = sim.get_feedback()
        print(result)

        if completed_task:
            pass
            #either break form loop or generate next task, e.g. update coordinates to fly to

    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()
