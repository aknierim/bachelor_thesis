"""
A simple function to create a colormap for a passed list of colors.
"""
import matplotlib.pyplot as plt
import numpy as np
from colour import Color
from matplotlib.colors import LinearSegmentedColormap

def custom_cmap(color_list: list) -> LinearSegmentedColormap:
    """Creates a colormap to a given list of colors.
    Also provides a preview of the colormap via plt.imshow().

    Parameters:
    -----------
    ramp_colors: list
        List of hexadecimal color codes with leading number sign (#).

    Returns:
    --------
    cmap: LinearSegmentedColormap
        A colormap containing the given colors.
    """

    cmap = LinearSegmentedColormap.from_list(
        'my_list', [Color(c1).rgb for c1 in color_list]
    )
    plt.figure(figsize = (15,3))
    plt.imshow(
        [list(np.arange(0, len(color_list), 0.1))],
        interpolation='nearest',
        origin='lower',
        cmap=cmap
    )
    plt.xticks([])
    plt.yticks([])

    return cmap