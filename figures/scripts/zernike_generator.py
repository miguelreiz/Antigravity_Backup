import numpy as np
import matplotlib.pyplot as plt
from scipy.special import zernike

def plot_zernike_psf(n, m, name, ax_phase, ax_psf):
    # Grid settings
    x = np.linspace(-1, 1, 200)
    y = np.linspace(-1, 1, 200)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    Theta = np.arctan2(Y, X)
    
    # Mask aperture
    mask = R <= 1
    
    # Calculate Zernike Polynomial (Phase)
    # Note: Scipy's zernike is radial, we need to combine with angular
    # This is a simplified placeholder logic for the standard Zernike definition
    # Z = R_n^m(r) * cos(m*theta)
    
    # For simulation purposes, we define simple shapes for key aberrations
    Z = np.zeros_like(R)
    if n==2 and m==0: Z = 2*R**2 - 1 # Defocus
    elif n==3 and m==-1: Z = (3*R**3 - 2*R) * np.sin(Theta) # Vertical Coma
    elif n==3 and m==-3: Z = R**3 * np.sin(3*Theta) # Trefoil
    elif n==4 and m==0: Z = 6*R**4 - 6*R**2 + 1 # Spherical
    
    Z[~mask] = np.nan
    
    # Plot Phase Map
    ax_phase.imshow(Z, cmap='jet', extent=[-1,1,-1,1])
    ax_phase.set_title(f"Phase: {name}", color='white')
    ax_phase.axis('off')
    
    # Calculate PSF (Fourier Transform of Aperture Function)
    Aperture = np.exp(1j * 2 * np.pi * Z) * mask
    PSF = np.abs(np.fft.fftshift(np.fft.fft2(Aperture)))**2
    
    # Plot PSF
    ax_psf.imshow(PSF, cmap='inferno', extent=[-1,1,-1,1])
    ax_psf.set_title(f"PSF: {name}", color='white')
    ax_psf.axis('off')
    # Zoom in on center
    ax_psf.set_xlim(-0.2, 0.2)
    ax_psf.set_ylim(-0.2, 0.2)

# Main Execution
plt.style.use('dark_background')
fig, axes = plt.subplots(2, 4, figsize=(16, 8))

# Define aberrations to plot
aberrations = [
    (2, 0, "Defocus (Miopia)"),
    (3, -1, "Coma Vertical"),
    (3, -3, "Trefoil"),
    (4, 0, "Aberr. Esférica")
]

for i, (n, m, name) in enumerate(aberrations):
    plot_zernike_psf(n, m, name, axes[0, i], axes[1, i])

plt.tight_layout()
plt.savefig('zernike_physics_simulation.png', dpi=300)
print("Simulation complete. Image saved.")
