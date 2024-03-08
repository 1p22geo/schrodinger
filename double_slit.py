import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import imageio.v2 as imageio

# Constants and parameters
Lx = 10.0  # Size of the domain in x-direction
Ly = 10.0  # Size of the domain in y-direction
Nx = 1000  # Number of spatial points in x-direction
Ny = 1000  # Number of spatial points in y-direction
Nt = 3000  # Number of time points
T_max = 200  # Maximum time
dt = T_max / Nt  # Time step
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y)
dx = x[1] - x[0]
dy = y[1] - y[0]

# Define the potential function (you can modify this)
V = np.zeros((Nx, Ny))
V[:,:] = 0
V[:, int(3.5* Ny // 8): int(4 * Ny // 8)] = 1000000
V[int(2.7*Nx / 7): int(3.2*Nx / 7), :] = 0
V[int(3.8*Nx / 7): int(4.3*Nx / 7), :] = 0

# Initial wave function (Gaussial wave packet)
sigma = 0.5
kx0 = 2.0
ky0 = 2.0
x0 = 2.0
y0 = 5.0
psi = np.exp(-((X - x0)**2 + (Y - y0)**2) / (2 * sigma**2)) * np.exp(1j * (kx0 * X + ky0 * Y))


# Create a directory to store the PNG images
import os
if not os.path.exists("output_images"):
    os.makedirs("output_images")

# Lists to store the frames for the video
frames = []

# Time evolution loop
for t in range(Nt):
    print(f"Time: {t}")
    # Calculate the new wave function using the Schrödinger equation
    psi = psi * np.exp(-1j * V * dt / 2)
    psi = np.fft.fft2(psi)
    psi = psi * np.exp(-1j * (np.fft.fftfreq(Nx, dx)**2 + np.fft.fftfreq(Ny, dy)**2) * dt)
    psi = np.fft.ifft2(psi)
    psi = psi * np.exp(-1j * V * dt / 2)

    # Calculate the real and imaginary components of the wave function
    real_part = np.absolute(psi)
    imag_part = np.angle(psi)

    # Create a figure with subplots for 3D projections
    fig = plt.figure(figsize=(12, 4))

    # 3D plot of real part
    ax1 = fig.add_subplot(131)
    ax1.pcolormesh(X, Y, real_part)
    ax1.set_title('Absolute')
    
    ax1.set_xlim(0, Lx)
    ax1.set_ylim(0, Ly)

    # 3D plot of imaginary part
    ax2 = fig.add_subplot(132)
    ax2.pcolormesh(X, Y, imag_part)
    ax2.set_title('Angle')
    
    ax2.set_xlim(0, Lx)
    ax2.set_ylim(0, Ly)

    # 3D plot of potential function
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.plot_surface(X, Y, V)
    ax3.set_title('Potential Function')
    
    ax3.set_xlim(0, Lx)
    ax3.set_ylim(0, Ly)
    #ax3.set_zlim(-1,1)

    # Save the figure as a PNG
    filename = f'output_images/frame_{t:03d}.png'
    plt.savefig(filename)
    print(f"Saved to {filename}")
    plt.close()

    frames.append(imageio.imread(filename))
    
# Create an animated GIF from the frames
imageio.mimsave('wave_animation.gif', frames, duration=0.1)

print("Done! Saved PNG images and created an animated GIF.")