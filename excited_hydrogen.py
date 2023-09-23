import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import imageio.v2 as imageio
import scipy

# Bohr radius
a0 = 1

# Constants and parameters
Lx = 20.0  # Size of the domain in x-direction
Ly = 20.0  # Size of the domain in y-direction
Nx = 2000  # Number of spatial points in x-direction
Ny = 2000  # Number of spatial points in y-direction
Nt = 4000  # Number of time points
T_max = 300  # Maximum time
dt = T_max / Nt  # Time step
x = np.linspace(0, Lx, Nx)
y = np.linspace(0, Ly, Ny)
X, Y = np.meshgrid(x, y)
dx = x[1] - x[0]
dy = y[1] - y[0]

# Define the potential function (central Coulomb potential)
x_center = Lx / 2
y_center = Ly / 2
r = np.sqrt((X - x_center)**2 + (Y - y_center)**2)
V = -1 / r  # Central Coulomb potential

# Initial wave function (electron in a p-orbital)
n = 2  # Principal quantum number
l = 1  # Angular momentum quantum number for p-orbital
m = 0  # Magnetic quantum number
r_norm = r / (n * a0)  # Normalize r for the excited state
theta = np.arctan2(Y - y_center, X - x_center)
# phi = np.zeros_like(theta)  # Azimuthal angle (0 for simplicity)
phi = theta
Ylm = scipy.special.sph_harm(m, l, theta, phi)  # Spherical harmonic
psi = (2 / (n * a0)**(3/2)) * r_norm * np.exp(-r_norm) * Ylm



real_part = np.real(psi)
imag_part = np.imag(psi)

# Create a figure with subplots for 3D projections
fig = plt.figure(figsize=(12, 4))

# 3D plot of real part
ax1 = fig.add_subplot(131, projection='3d')
ax1.plot_surface(X, Y, real_part, cmap='viridis')
ax1.set_title('Real Part')

ax1.set_xlim(0, Lx)
ax1.set_ylim(0, Ly)
ax1.set_zlim(-0.5, 0.5)

# 3D plot of imaginary part
ax2 = fig.add_subplot(132, projection='3d')
ax2.plot_surface(X, Y, imag_part, cmap='viridis')
ax2.set_title('Imaginary Part')

ax2.set_xlim(0, Lx)
ax2.set_ylim(0, Ly)
ax2.set_zlim(-0.5, 0.5)

# 3D plot of potential function
ax3 = fig.add_subplot(133, projection='3d')
ax3.plot_surface(X, Y, V)
ax3.set_title('Potential Function')

ax3.set_xlim(0, Lx)
ax3.set_ylim(0, Ly)
ax3.set_zlim(-0.5, 0.5)

# Save the figure as a PNG
filename = f'output_images5/frame_test.png'
plt.savefig(filename)
print(f"Saved to {filename}")
plt.close()


# Create a directory to store the PNG images
import os
if not os.path.exists("output_images5"):
    os.makedirs("output_images5")

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
    real_part = np.real(psi)
    imag_part = np.imag(psi)

    # Create a figure with subplots for 3D projections
    fig = plt.figure(figsize=(12, 4))

    # 3D plot of real part
    ax1 = fig.add_subplot(131, projection='3d')
    ax1.plot_surface(X, Y, real_part, cmap='viridis')
    ax1.set_title('Real Part')
    
    ax1.set_xlim(0, Lx)
    ax1.set_ylim(0, Ly)
    ax1.set_zlim(-0.5, 0.5)

    # 3D plot of imaginary part
    ax2 = fig.add_subplot(132, projection='3d')
    ax2.plot_surface(X, Y, imag_part, cmap='viridis')
    ax2.set_title('Imaginary Part')
    
    ax2.set_xlim(0, Lx)
    ax2.set_ylim(0, Ly)
    ax2.set_zlim(-0.5, 0.5)

    # 3D plot of potential function
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.plot_surface(X, Y, V)
    ax3.set_title('Potential Function')
    
    ax3.set_xlim(0, Lx)
    ax3.set_ylim(0, Ly)
    ax3.set_zlim(-0.5, 0.5)

    # Save the figure as a PNG
    filename = f'output_images5/frame_{t:03d}.png'
    plt.savefig(filename)
    print(f"Saved to {filename}")
    plt.close()

    frames.append(imageio.imread(filename))
    
# Create an animated GIF from the frames
imageio.mimsave('wave_animation5.gif', frames, duration=0.1)

print("Done! Saved PNG images and created an animated GIF.")