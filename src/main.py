import os
import glob

import numpy as np
from scipy.interpolate import interp1d

from utils.helper import trimmed_signal, get_signal_times
from utils.data_set_of_gramian_angular_fields import show_gaf_image, save_gaf_image
from utils.data_set_of_markov_transition_fields import show_mtf_image
from utils.data_set_of_recurrence_plots import show_rp_images


BASE_DIR = 'seismic_signals'
RESAMPLED_LENGTH = 1024

def main():
    signal_dirs = [os.path.join(BASE_DIR, d) for d in os.listdir(BASE_DIR)]
    signals_times_rp =[]
    signals = []
    durations = []
    
    for signal_dir in signal_dirs:
        # Load .txt file (assumes there's only one per folder)
        txt_file = glob.glob(os.path.join(signal_dir, '*.txt'))[0]
        signal = np.loadtxt(txt_file).astype(float).flatten()
       
        # Load .xlsx file (assumes there's only one per folder)
        xlsx_file = glob.glob(os.path.join(signal_dir, '*.xls'))[0]
      
        signal = trimmed_signal(signal)
        times = get_signal_times(xlsx_file, len(signal))

        durations.append(times[-1] - times[0])
        signals_times_rp.append((signal, times))
        
        #### Interpolate to uniform length####
        # Create interpolation function from irregular times series
        f_interp = interp1d(times, signal, kind='linear', fill_value='extrapolate')
        # Define uniform times steps (fixed length)
        times_uniform = np.linspace(times.min(), times.max(), RESAMPLED_LENGTH)
        #Get the resampled signal
        signal_resampled = f_interp(times_uniform)
        signals.append(signal_resampled)
        
    signals_array = np.array(signals)

    #show_gaf_image(signals_array)
    #show_mtf_image(signals_array)
    #show_rp_images(durations, signals_times_rp, RESAMPLED_LENGTH)

  
if __name__ == "__main__":
    main()
