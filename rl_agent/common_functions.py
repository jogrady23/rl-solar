import numpy as np

# Set default constants for problem
ARRAY_DIMENSION_TUPLE = (37,37)
MOTOR_ANGLE_POWER_DRAW = 0.0001

def rolling_avg_calc(value, last_value, window):
    """
    Calculates a rolling average
    
    Args:
        value (float): the latest value to add to the rolling avg
        last_value (float): the last value from the calculation
        window (int): the number of samples to take the avg over
    Returns:
        float: the rolling avg value
    """
    return (1/window)*value + (1-(1/window))*last_value

# Converts between index types

def convert_motor_positions_to_2d_index(position_tuple):
    # position tuple is (m1 position, m2 position)
    return (int(position_tuple[0]//5), int(position_tuple[1]//5))

def convert_2d_index_to_motor_positions(index_tuple):
    return (index_tuple[0]*5, index_tuple[1]*5)

def convert_1d_index_to_2d_index(index, dimensions=ARRAY_DIMENSION_TUPLE):
    return np.unravel_index(index, dimensions)

def convert_2d_index_to_1d_index(index_tuple, dimensions=ARRAY_DIMENSION_TUPLE):
    return np.ravel_multi_index(index_tuple, dimensions)

def convert_motor_positions_to_1d_index(position_tuple, dimensions=ARRAY_DIMENSION_TUPLE):
    return convert_2d_index_to_1d_index(convert_motor_positions_to_2d_index(position_tuple), dimensions)

def convert_1d_index_to_motor_positions(index, dimensions=ARRAY_DIMENSION_TUPLE):
    return convert_2d_index_to_motor_positions(convert_1d_index_to_2d_index(index, dimensions))