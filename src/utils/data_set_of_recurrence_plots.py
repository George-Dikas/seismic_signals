import numpy as np
from scipy.interpolate import interp1d
from pyts.image import RecurrencePlot
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid


def get_final_signals(durations, signals_times_rp, resampled_length: int) -> np.ndarray:
    """

    Args:
        durations (float):
        signals_times_rp:
        resampled_length"

    Returns:
        np.ndarray: 
    """
    
    min_duration = min(durations)
    print(f"Minimum common time duration: {min_duration:.3f} sec")

    signals_resampled = []

    for signal, times in signals_times_rp:
        end_time = times[0] + min_duration
        mask = times <= end_time
        times_cut = times[mask]
        signal_cut = signal[mask]

        f_interp = interp1d(times_cut, signal_cut, kind='linear', fill_value='extrapolate')
        times_uniform = np.linspace(times_cut[0], times_cut[-1], resampled_length)
        signal_resampled = f_interp(times_uniform)
        signals_resampled.append(signal_resampled)

    return np.array(signals_resampled)

def show_rp_images(durations, signals_times_rp, resampled_length):
    """
    Generates and displays Recurrence Plots (RP) images for a collection 
    of time-series signals. The function transforms each signal into a 2D RP 
    image and visualizes up to 100 of them in a 10×10 grid using Matplotlib.

    Args:
        signals_array (np.ndarray): 2D array of seismic signal values.
    """
    
    rp = RecurrencePlot(threshold='point', percentage=20)
    signals_array = get_final_signals(
        durations, 
        signals_times_rp, 
        resampled_length
    )
    X_rp = rp.fit_transform(signals_array)

    fig = plt.figure(figsize=(15, 15))
    grid = ImageGrid(fig, 111, nrows_ncols=(10, 10), axes_pad=0.2, share_all=True)

    for i, ax in enumerate(grid[:len(X_rp)]):
        ax.imshow(X_rp[i], cmap='binary', origin='lower')
        ax.set_xticks([])
        ax.set_yticks([])

    fig.suptitle("Recurrence Plots of 100 Signals (Aligned in Time)", y=0.92, 
                fontsize=16)
    plt.show()