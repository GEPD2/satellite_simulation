#Library for multidimentional arrays and more
import numpy as np
#Time library
import time
#Library for random numbers (for pseudo random numbers)
import random
#Library for ploting the final graph (after compliting the circular orbit)
import matplotlib.pyplot as plt
#Library named tqdm is used for the progress bar
from tqdm import tqdm
#Constants
#Gravitational constant (m^3 kg^-1 s^-2)
G = 6.67430e-11
#Mass of Earth (kg)
M = 5.972e24
#Radius of Earth (m)
R = 6371e3
#Satellite mass (kg)
satellite_mass = 500   
#Communication Parameters
#Bandwidth (bits per second)
bandwidth = 1e6 
#Packet size in bits (1 KB)
packet_size = 1024 * 8
#Time to send one packet (seconds)
transmission_speed = packet_size / bandwidth
#Propagation delay for LEO satellite (~5 ms)
propagation_delay = 0.005  
#Initial orbital parameters
#Initial position (7000 km from Earth's center)
x0, y0 = 7000e3, 0  
vx0, vy0 = 0, 7.12e3  # Initial velocity (7.12 km/s for a circular orbit)
dt = 10  # Time step in seconds
T = 2 * np.pi * 7000e3 / 7.12e3  # Orbital period (seconds)
# Function to update satellite's orbit (position and velocity)
def update_orbit(x, y, vx, vy, dt):
    """
    This function updates the position and velocity of the satellite based on orbital mechanics.
    Parameters:
    - x, y: Current position of the satellite (in meters)
    - vx, vy: Current velocity of the satellite (in meters per second)
    - dt: Time step for updating the position (in seconds)
    It returns -> Updated position and velocity
    """
    #Computation of the distance from Earth's center (r)
    r = np.sqrt(x**2 + y**2)
    # omputation of the gravitational force (F = G * M * m / r^2)
    F = G * M * satellite_mass / r**2 
    #Computation of the acceleration in the x and y directions
    ax = -F * x / (r * satellite_mass)  # Acceleration in x direction
    ay = -F * y / (r * satellite_mass)  # Acceleration in y direction
    #Update the velocity based on acceleration
    vx += ax * dt
    vy += ay * dt
    #Update the position based on the new velocity
    x += vx * dt
    y += vy * dt 
    return x, y, vx, vy
#Function to simulate data transfer with delay
'''
Data Transfer Parameters:
Transmission Power -> Simulating how much data the satellite can transmit.
Data Packet Size -> Divide the data into packets.
Transmission Speed -> Based on the bandwidth, simulating how long it takes to send each packet.
Propagation Delay -> Simulating the time it takes for a signal to travel from the satellite to Earth.
'''
def simulate_data_transfer(num_packets=4):
    global total
    for i in tqdm(range(num_packets), desc="Transmitting packets", ncols=100, unit="packet"):
        total+=1
        # Simulate propagation delay (time taken for signal to reach Earth)
        time.sleep(propagation_delay)
        
        # Simulate transmission time (time to send one packet)
        time.sleep(transmission_speed)
        
        # Random delay between packets to simulate real-world variations
        random_delay = random.uniform(0.1, 0.5)  # Random delay between packets
        time.sleep(random_delay)
total=0
#Function for full simulation loop
def simulate_satellite_system(packets_number):
    #Initialize variables
    x, y, vx, vy = x0, y0, vx0, vy0
    #Number of steps to simulate
    time_steps = 1000  
    x_positions = []
    y_positions = []
    print("Starting satellite system simulation...")
    #Simulating satellite orbit and communication
    for step in range(time_steps):
        #Update satellite's position and velocity
        x, y, vx, vy = update_orbit(x, y, vx, vy, dt)
        #Store position for plotting
        x_positions.append(x)
        y_positions.append(y)
        #Simulate data transfer every 100th step (as an example)
        if step % 100 == 0:
            #Send number of packets every 100th step
            simulate_data_transfer(num_packets=packets_number)  
    print("Satellite system simulation complete!\n")
    print("total packets transfered {}\n".format(total))
    # Plot the orbit of the satellite
    plt.plot(x_positions, y_positions)
    plt.title("Satellite Orbit")
    plt.xlabel("x Position (m)")
    plt.ylabel("y Position (m)")
    plt.axis("equal")
    plt.grid(True)
    plt.show()
#give parameters
packets_number=int(input("Give the number of packets transmiting each time\n"))
#Running the simulation
simulate_satellite_system(packets_number=packets_number)
#in the end a plot of the full orbit will appear
