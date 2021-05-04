# shared.py
#
# Codixi spartziu intra is àteras mitzas in Python.
# Shared code between the other Python sources.
#
# Copyright 2021 The Sardinia Computational Sustainability Initiative
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import matplotlib.pyplot as plt
import os


def save_figure(output_file_name):
    figures_folder = "../figures/"
    if not os.path.exists(figures_folder):
        os.makedirs(figures_folder)
    plt.savefig(figures_folder + output_file_name + ".png", dpi=150)
    plt.savefig(figures_folder + output_file_name + ".pgf")