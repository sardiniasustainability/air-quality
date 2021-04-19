# Shared code

import matplotlib.pyplot as plt
import os


def save_figure(output_file_name):
    figures_folder = "../figures/"
    if not os.path.exists(figures_folder):
        os.makedirs(figures_folder)
    plt.savefig(figures_folder + output_file_name, dpi=150)
