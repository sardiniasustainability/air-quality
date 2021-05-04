# yearly_data_analysis.py
#
# Analisa is dadus de is imitiduras a s' annu.
# Analyse yearly emission data.
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

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os
from functools import reduce
import shared


def _select_pollutant_and_comune_data(pollution_data, pollutant_name, comuni_names):
    """ Select the rows in the dataframe that refer to the given pollutant
        and province
    """
    # Clean the "Comune" column
    for comune in comuni_names:
        comune.title()
    pollution_data.set_index('Comune')
    pollution_data.Comune = pollution_data.Comune.str.title()

    data_by_pollutant = pollution_data.loc[
        (pollution_data['Inquinante'] == pollutant_name) &
        (pollution_data['Comune'].isin(comuni_names))].copy()

    # Delete now-implicit data
    data_by_pollutant.pop('Inquinante')
    data_by_pollutant.pop('Provincia')

    # Rename the "Valore" column to "Macrosettore"
    category = data_by_pollutant.Macrosettore.unique()
    data_by_pollutant.rename(
        columns={'Valore': category[0]}, inplace=True)
    data_by_pollutant.pop('Macrosettore')
    return data_by_pollutant


def _read_pollutant_data_in_file(file_name, pollutant_name, comuni_names):
    """ Given a pollutant and the names of Comuni, read the data from the file 
        and select the desired rows
    """
    pollutant_data = pd.read_csv(file_name)
    pollutant_data = _select_pollutant_and_comune_data(
        pollutant_data, pollutant_name, comuni_names)
    return pollutant_data


def _read_all_pollutant_data(pollutant, comuni_names):
    """ Read all the available pollutant data across multiple files and comune
    """
    # Read data from the files
    base_path = "../data/yearly_emissions"
    all_data = [_read_pollutant_data_in_file(file_name, pollutant, comuni_names)
                for file_name in Path(base_path).glob('*.csv')]
    return _join_multiple(all_data)


def _join_multiple(dataframes):
    """ Join multiple tables into one
    """
    joined_tables = reduce(
        lambda left, right: pd.merge(left, right), dataframes)
    return joined_tables


def _plot_pollutant_origin_breakdown(pollutant, comuni_names, file_name):
    """ Read and plot the data for the given pollutant and the given comunis
    """
    # Read data from the files
    total_data = _read_all_pollutant_data(pollutant, comuni_names)

    # Plot stacked bar plot
    ax = total_data.plot.barh(stacked=True)
    plot_size = shared.figure_size(.8, .7)
    ax.figure.set_size_inches(*plot_size)
    ax.set_yticklabels(total_data["Comune"])
    ax.set_xlabel(pollutant)
    ax.set_ylabel(total_data.index.name)
    ax.set_title("Particulate emissions in the  Metropolitan City of Cagliari")
    ax.invert_yaxis()
    ax.legend(loc="lower left")

    # Add margin to center content
    fig = plt.gcf()
    image_height = plot_size[1]
    image_width = plot_size[0]
    image_left_margin = 1.5/image_width
    image_right_margin = 3/image_width
    fig.set_size_inches(image_width, image_height)
    plt.subplots_adjust(left=image_left_margin, right=image_right_margin)

    # Save figures
    shared.save_figure(file_name)


def _read_comuni_cagliari():
    """ Read the Comuni of interest for most plots: those in the Province of Cagliari
    """
    with open('../data/comuni/focus_comuni_provincia_cagliari.txt') as f:
        lines = f.read().splitlines()
    return lines


def _associate_geographic_data(pollution_data):
    """ Add geographic data to yearly pollution data for plotting
    """
    import geopandas as gp
    map_data = gp.read_file('../data/geo/comune-limits.shp')
    pollution_data['Comune'] = [name.upper()
                                for name in pollution_data['Comune']]
    merged_map = map_data.merge(pollution_data,
                                how="inner",
                                left_on="nome",
                                right_on="Comune")
    return merged_map


def _plot_pollutant_map(pollutant, comuni_names, file_name):
    """ Plot pollution data on the map of Sardinia
    """
    # Read data from the files
    total_data = _read_all_pollutant_data(pollutant, comuni_names)
    # Sum through pollutant origins
    total_data['Total'] = total_data.iloc[:, 1:].sum(axis=1)

    total_data = _associate_geographic_data(total_data)

    # Generate plot
    _, ax = plt.subplots(figsize=shared.figure_size(.7, 1.33))
    plt.tick_params(left=False,
                    bottom=False,
                    labelleft=False,
                    labelbottom=False)
    total_data.plot(column="Total",
                    cmap='OrRd',
                    ax=ax,
                    linewidth=0.8,
                    edgecolor='0.1',
                    legend=True)
    ax.set_title(
        "Particulate emissions in the Metropolitan City of Cagliari:\n" + pollutant)

    # Save figures
    shared.save_figure(file_name)


shared.set_font_defaults()

comuni = _read_comuni_cagliari()
_plot_pollutant_origin_breakdown("PM2,5 ( Mg ) ", comuni, "pm25")
_plot_pollutant_origin_breakdown("PM10 ( Mg ) ", comuni, "pm10")

_plot_pollutant_map("PM2,5 ( Mg ) ", comuni, "pm25_map")
_plot_pollutant_map("PM10 ( Mg ) ", comuni, "pm10_map")
