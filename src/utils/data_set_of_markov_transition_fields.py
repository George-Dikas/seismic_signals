from pyts.image import MarkovTransitionField
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid


N_BINS = 8

def show_mtf_image(signals_array):
    """
    Generates and displays Markov Trasition Field (MTF) images for a collection 
    of time-series signals. The function transforms each signal into a 2D MTF 
    image and visualizes up to 100 of them in a 10×10 grid using Matplotlib.

    Args:
        signals_array (np.ndarray): 2D array of seismic signal values.
    """

    # Compute  Markov Transition Field
    mtf = MarkovTransitionField(n_bins=N_BINS)
    signals_mtf = mtf.fit_transform(signals_array)

    # Plotting all 100 signals in a 10x10 grid ===
    n_signals = len(signals_mtf)
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
            signals_mtf[i], 
            cmap='rainbow', 
            origin='lower', 
            vmin=0., 
            vmax=1.
        )
        ax.set_xticks([])
        ax.set_yticks([])

    plt.colorbar(im, cax=grid.cbar_axes[0])
    #grid.cbar_axes[0].toggle_label(True)
    ax.cax.yaxis.label.set_visible(True)

    fig.suptitle(
        "Markov Transition Fields of 100 Seismic Signals", 
        y=0.92, 
        fontsize=16
    )
    plt.show()
    