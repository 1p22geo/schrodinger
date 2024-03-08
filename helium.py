import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import imageio.v2 as imageio
import scipy
import math
import lib

config = lib.QuantumConfig(1, 16, 16, 2000, 2000, 4000, 300)

# a0 = 1
# # Constants and parameters
# Lx = 16.0  # Size of the domain in x-direction
# Ly = 16.0  # Size of the domain in y-direction
# Nx = 2000  # Number of spatial points in x-direction
# Ny = 2000  # Number of spatial points in y-direction
# Nt = 4000  # Number of time points
# T_max = 300  # Maximum time
# dt = T_max / Nt  # Time step
# x = np.linspace(0, Lx, Nx)
# y = np.linspace(0, Ly, Ny)
# X, Y = np.meshgrid(x, y)
# dx = x[1] - x[0]
# dy = y[1] - y[0]

# Define the potential function (central Coulomb potential)

potential = lib.CoulombPotential(config)



el1 = lib.Electron(config, potential, 2, 1, 0)

el2 = lib.Electron(config, potential, 2, 1, 0)
el2.psi *= -1

# n = 2  # Principal quantum number
# l = 1  # Angular momentum quantum number for p-orbital
# m = 0  # Magnetic quantum number
# r_norm = r / (n * a0)  # Normalize r for the excited state
# theta = np.arctan2(Y - y_center, X - x_center)
# # phi = np.zeros_like(theta)  # Azimuthal angle (0 for simplicity)
# phi = theta
# Ylm = scipy.special.sph_harm(m, l, theta, phi)  # Spherical harmonic
# psi1 = (2 / (n * a0)**(3/2)) * r_norm * np.exp(-r_norm) * Ylm


# n2 = 2  # Principal quantum number
# l2 = 1  # Angular momentum quantum number for p-orbital
# m2 = 0  # Magnetic quantum number
# r_norm2 = r / (n2 * a0)  # Normalize r for the excited state
# theta2 = -np.arctan2(Y - y_center, X - x_center)
# # phi = np.zeros_like(theta)  # Azimuthal angle (0 for simplicity)
# phi2 = theta2
# Ylm2 = -scipy.special.sph_harm(m2, l2, theta2, phi2)  # Spherical harmonic
# psi2 = (2 / (n2 * a0)**(3/2)) * r_norm2 * np.exp(-r_norm2) * Ylm2

# Initialize the electron wave functions
# psi1 = np.exp(-r) / np.sqrt(np.pi)  # Ground state of hydrogen atom for electron 1
# psi2 = np.exp(-r) / np.sqrt(np.pi)  # Ground state of hydrogen atom for electron 2

# Create a directory to store the PNG images
import os
if not os.path.exists("output_images4"):
    os.makedirs("output_images4")

# Lists to store the frames for the video
frames = []

# Time evolution loop
for t in range(config.Nt):
    print(f"Time: {t}")
    # Calculate the mean-field potential from the other electron
    p1 = lib.MeanFieldPotential(config, el2)
    p2 = lib.MeanFieldPotential(config, el1)

    # Calculate the new wave function using the Schrödinger equation with mean-field potential
    el1.propagate(potential.V + p1.V)
    el2.propagate(potential.V + p2.V)
    # psi1 = psi1 * np.exp(-1j * (V + V_mean_field) * dt / 2)
    # psi1 = np.fft.fft2(psi1)
    # psi1 = psi1 * np.exp(-1j * (np.fft.fftfreq(Nx, dx)**2 + np.fft.fftfreq(Ny, dy)**2) * dt)
    # psi1 = np.fft.ifft2(psi1)
    # psi1 = psi1 * np.exp(-1j * (V + V_mean_field) * dt / 2)

    # psi2 = psi2 * np.exp(-1j * (V + V_mean_field) * dt / 2)
    # psi2 = np.fft.fft2(psi2)
    # psi2 = psi2 * np.exp(-1j * (np.fft.fftfreq(Nx, dx)**2 + np.fft.fftfreq(Ny, dy)**2) * dt)
    # psi2 = np.fft.ifft2(psi2)
    # psi2 = psi2 * np.exp(-1j * (V + V_mean_field) * dt / 2)
    
    # Integrate the variable

    # Calculate the real and imaginary components of the wave functions
    real_part1 = np.angle(el1.psi)
    imag_part1 = np.absolute(el1.psi)
    real_part2 = np.angle(el2.psi)
    imag_part2 = np.absolute(el2.psi)

    # Create a figure with subplots for 3D projections
    fig = plt.figure(figsize=(12, 8))

    # 3D plot of real part for electron 1
    ax1 = fig.add_subplot(231)
    cs = ax1.contourf(config.X, config.Y, real_part1)
    ax1.set_title('Angle (Electron 1)')
    ax1.set_xlim(0, config.Lx)
    ax1.set_ylim(0, config.Ly)
    cbar = fig.colorbar(cs)

    # 3D plot of imaginary part for electron 1
    ax2 = fig.add_subplot(234, projection='3d')
    ax2.plot_surface(config.X, config.Y, imag_part1, cmap='viridis')
    ax2.set_title('Absolute (Electron 1)')
    ax2.set_xlim(0, config.Lx)
    ax2.set_ylim(0, config.Ly)

    # 3D plot of real part for electron 2
    ax3 = fig.add_subplot(232)
    cs2 = ax3.contourf(config.X, config.Y, real_part2)
    ax3.set_title('Angle (Electron 2)')
    ax3.set_xlim(0, config.Lx)
    ax3.set_ylim(0, config.Ly)
    cbar2 = fig.colorbar(cs2)

    # 3D plot of imaginary part for electron 2
    ax4 = fig.add_subplot(235, projection='3d')
    ax4.plot_surface(config.X, config.Y, imag_part2, cmap='viridis')
    ax4.set_title('Absolute (Electron 2)')
    ax4.set_xlim(0, config.Lx)
    ax4.set_ylim(0, config.Ly)
    
    ax4 = fig.add_subplot(233, projection='3d')
    ax4.plot_surface(config.X, config.Y, p1.V)
    ax4.set_title('Potential mean field')
    ax4.set_xlim(0, config.Lx)
    ax4.set_ylim(0, config.Ly)
    ax4.set_zlim(-0.5, 0.5)
    
    ax4 = fig.add_subplot(236, projection='3d')
    ax4.plot_surface(config.X, config.Y, potential.V)
    ax4.set_title('Potential function')
    ax4.set_xlim(0, config.Lx)
    ax4.set_ylim(0, config.Ly)
    ax4.set_zlim(-0.5, 0.5)

    # Save the figure as a PNG
    filename = f'output_images4/frame_{t:03d}.png'
    plt.savefig(filename)
    print(f"Saved to {filename}")
    plt.close()

    frames.append(imageio.imread(filename))

# Create an animated GIF from the frames
imageio.mimsave('wave_animation4.gif', frames, duration=0.1)

print("Done! Saved PNG images and created an animated GIF.")
