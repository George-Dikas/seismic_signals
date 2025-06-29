import os

import numpy as np
from pyts.image import GramianAngularField
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid


def show_gaf_image(signals_array: np.ndarray) -> None:
    """
    Generates and displays Gramian Angular Field (GAF) images for a collection 
    of time-series signals. The function transforms each signal into a 2D GAF 
    image and visualizes up to 100 of them in a 10×10 grid using Matplotlib.

    Args:
        signals_array (np.ndarray): 2D array of seismic signal values.
    """

    # Compute Gramian Angular Fields
    gaf = GramianAngularField()
    signals_gaf = gaf.fit_transform(signals_array)
    
    # Plotting all 100 signals in a 10x10 grid ===
    n_signals = len(signals_gaf)
    n_plot = min(100, n_signals) # plot up to 100 signals

    fig = plt.figure(figsize=(15, 15))
    grid = ImageGrid(
        fig, 
        111, 
        nrows_ncols=(10, 10), 
        axes_pad=0.2, 
        share_all=True, 
        cbar_mode='single'
    )

    for i, ax in enumerate(grid[:n_plot]):
        im = ax.imshow(
            signals_gaf[i], 
            cmap='rainbow', 
            origin='lower', 
            vmin=-1., 
            vmax=1.
        )
        ax.set_xticks([])
        ax.set_yticks([])

    plt.colorbar(im, cax=grid.cbar_axes[0])
    #grid.cbar_axes[0].toggle_label(True)
    ax.cax.yaxis.label.set_visible(True)

    fig.suptitle(
        "Gramian Angular Fields of 100 Seismic Signals", 
        y=0.92, 
        fontsize=16
    )
    plt.show()

def save_gaf_image(signals_array: np.ndarray) -> None:
    """
    Converts a 2D array of time-series signals into Gramian Angular Field (GAF) 
    images and saves them as PNG files.
    Each row of the input array is interpreted as an individual signal. The 
    function transforms each signal into a GAF image using the GramianAngularField 
    transformer from the pyts library and saves the resulting images in the 
    'output_gaf' directory.

    Args:
        signals_array (np.ndarray): 2D array of seismic signal values.
    """

    gaf = GramianAngularField()
    signals_gaf = gaf.fit_transform(signals_array)

    os.makedirs("output_gaf", exist_ok=True)
    
    for i, gaf_image in enumerate(signals_gaf):
        plt.imshow(gaf_image, cmap='rainbow', origin='lower', vmin=-1., vmax=1.)
        plt.axis('off')  # Hide axes
        plt.savefig(
            f"output_gaf/image_{i:03d}.png", 
            bbox_inches='tight', 
            pad_inches=0
        )
        plt.close()  # Prevent memory leaks