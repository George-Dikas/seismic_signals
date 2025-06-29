import numpy as np
import pandas as pd


def get_signal_times(xlsx_file, len_of_signal: int) -> np.ndarray:
    """
    The function reads all sheets in the Excel file and searches for the first sheet 
    that contains a column where the first row is zero. It then drops any NaN values, 
    flattens the resulting values into a list, and ensures the list is of length 
    `len_of_signal`. If the list is too short, new time values are extrapolated 
    using a simple linear pattern.

    Args:
        xlsx_file: Path to the Excel file or a file-like object.
        len_of_signal (int): Length of a seismic signal.

    Returns:
        np.ndarray: A 1D NumPy array containing seismic signal's time values.
    """
    
    all_sheets = pd.read_excel(xlsx_file, sheet_name=None, header=None)

    for sheet_name, df in all_sheets.items():
        if df.empty:
            continue

        filtered_df = df.loc[:, df.iloc[0] == 0]
        
        if filtered_df.columns.empty:
            continue
        df = filtered_df.dropna()
        break

    signal_times = df.values.flatten().tolist()
          
    if len(signal_times) >= len_of_signal:
        signal_times = signal_times[:len_of_signal]
    else:
        i = len(signal_times)
        
        while i < len_of_signal:
            signal_times.append(round(signal_times[1]+signal_times[i-1], 3))
            i += 1
    
    return np.array(signal_times)

def trimmed_signal(signal: np.ndarray) -> np.ndarray:
    """
    Trims low-magnitude values from the start and end of a seismic signal.
    Trimming stops when a value with sufficient magnitude is encountered.

    Args:
        signal (np.ndarray): 1D array of seismic signal values.

    Returns:
        signal (np.ndarray): 1D trimmed array of seismic signal values.
    """

    start_index = 0
    end_index = len(signal) - 1

    # while start_index < end_index and \
    # count_decimal_shifts(signal[start_index]) > 2:
    #     start_index += 1
    # print(signal[start_index])
    # while end_index > start_index and \
    # count_decimal_shifts(signal[start_index]) > 2:
    #     end_index += 1

    while start_index < end_index and \
    compare_with_threshold(signal[start_index]) == False:
        start_index += 1
    # print(start_index)
    while end_index > start_index and \
    compare_with_threshold(signal[start_index]) == False:
        end_index += 1

    return signal[start_index:end_index]
    
def count_decimal_shifts(val: float) -> int:
    """
    This function determines how many times a number less than 1 (but not 0)
    needs to be multiplied by 10 before it becomes greater than or equal to 1.
    
    Args:
        val (float): The input number. Can be negativeor positive.

    Returns:
        count (int): The number of decimal shifts (multiplications by 10) 
        required to bring the absolute value of `val` to 1 or more. Returns 0 if 
        `val` is 0 or >= 1.
    """
    
    val = abs(val)
    count = 0

    while val < 1 and val != 0:
        val *= 10
        count += 1
        
    return count

def compare_with_threshold(val: float) -> bool:
    """
    Compare a given float value with a predefined threshold.

    Args:
        val (float): The value to compare.

    Returns:
        bool: True if the value is greater than or equal to the threshold (0.03), 
              False otherwise.
    """
    
    threshold = 0.03
    
    if val >= threshold:
        return True
    return False
