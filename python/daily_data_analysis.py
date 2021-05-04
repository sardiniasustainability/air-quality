# daily_data_analysis
#
# Analisa is dadus de is imitiduras a sa dii.
# Analyse daily emission data.
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
import pandas as pd
import numpy as np
import datetime
import os
import shared


def _reindex_daily(data_series, year):
    """ Re-index a data series and fill missing measurements with nans
    """
    idx = pd.date_range('01-01-' + str(year), '12-31-' + str(year))
    data_series = data_series.reindex(idx, fill_value=np.nan)
    return data_series


def _reformat_monthly_data_by_day(montly_data, month_number, year):
    """ Reformat the data about a month into a time series by day
    """
    import math

    measurements = pd.to_numeric(montly_data.array, errors='coerce')
    day_of_month = pd.to_numeric(montly_data.index)

    new_measurements = []
    new_dates = []
    for meas, day in zip(measurements, day_of_month):
        # Remove the invalid or empty measurements
        if not math.isnan(meas):
            new_measurements.append(meas)
            new_dates.append(datetime.date(year, month_number, day+1))
    return pd.Series(new_measurements, index=new_dates)


def _convert_to_timeseries(daily_pollution_data, year):
    """ Convert the weird format used by the Sardegna Ambiente dataset
    """
    import datetime
    import pandas as pd

    # Exclude the "day of the month" column
    pollution_data = daily_pollution_data.iloc[:, 1:]

    data_series = pd.Series(dtype='float64')

    # Iterate through the months
    month = 1
    for curr_column in pollution_data.columns:
        curr_data = pollution_data[curr_column]
        month_series = _reformat_monthly_data_by_day(curr_data, month, year)
        month = month+1

        data_series = data_series.append(month_series)

    data_series = _reindex_daily(data_series, year)
    return data_series


def _plot_thresholds(thresholds, ax):
    """ Plot horizontal lines with threshold levels
    """
    if "WhoDaily" in thresholds:
        ax.axhline(y=thresholds["WhoDaily"], color='red',
                   linestyle='--', label="WHO daily threshold", linewidth=1)
    if "WhoYearly" in thresholds:
        ax.axhline(y=thresholds["WhoYearly"], color='magenta',
                   linestyle='--', label="WHO yearly threshold", linewidth=1)
    if "ItaDaily" in thresholds:
        ax.axhline(y=thresholds["ItaDaily"], color='red', linestyle=':',
                   label="Italian daily threshold", linewidth=1)
    if "ItaYearly" in thresholds:
        ax.axhline(y=thresholds["ItaYearly"], color='magenta', linestyle=':',
                   label="Italian yearly threshold", linewidth=1)


def _plot_daily_pollution_subplot(data_file_name, year, thresholds, ax, title=''):
    """ Plot the data about daily pollution
    """
    # Read data
    daily_pollution_data = pd.read_csv(
        "../data/daily_emissions/" + data_file_name, comment="#")
    daily_pollution_data = _convert_to_timeseries(daily_pollution_data, year)

    # Line plot
    daily_pollution_data.plot(label="Daily measurements", ax=ax, linewidth=1)
    ax.set_ylabel("Concentration (μg/m³)")
    ax.set_xlabel("Date")
    ax.set_title(title)
    ax.axhline(y=daily_pollution_data.mean(), color='black',
               linestyle='-', label="Yearly mean", linewidth=1)
    _plot_thresholds(thresholds, ax)

    # Reduce the number of xticks
    initial_xticks = ax.get_xticks(minor=False)
    new_xticks = initial_xticks[0::2]
    new_xticks = np.append(new_xticks, initial_xticks[-1])
    ax.set_xticks(new_xticks)
    ax.set_xticks([], minor=True)


def _plot_daily_pollution(data, output_file_name, title=''):
    """ Plot the data about daily pollution
    """
    import math

    num_plots = len(data)
    num_cols = min(2, num_plots)
    num_rows = math.ceil(num_plots/num_cols)
    single_plot_width = 0.48
    single_plot_ratio = 2
    _, axs = plt.subplots(num_rows, num_cols,
                          figsize=shared.figure_size(
                              single_plot_width*num_cols,
                              single_plot_ratio/num_rows))
    axs = axs.reshape(-1).tolist()

    for curr_data, curr_ax in zip(data, axs):
        _plot_daily_pollution_subplot(
            curr_data['file'], curr_data['year'], curr_data['thresholds'], curr_ax, curr_data['title'])

    # Save figure
    shared.save_figure(output_file_name)


pm25_thresholds = {
    "WhoYearly": 10,
    "WhoDaily": 25+0.1,
    "ItaYearly": 25-0.1
}
pm10_thresholds = {
    "WhoYearly": 20,
    "WhoDaily": 50+0.1,
    "ItaYearly": 40,
    "ItaDaily": 50-0.1
}

shared.set_font_defaults()

# Monserrato
monserrato_data = [
    {
        'file': "CENMO1-Anno-2019-PM2.5.csv",
        'year': 2019,
        'thresholds': pm25_thresholds,
        'title': "PM 2.5 emissions 2019"
    }, {
        'file': "CENMO1-Anno-2019-PM10.csv",
        'year': 2019,
        'thresholds': pm10_thresholds,
        'title': "PM 10 emissions in 2019"
    }, {
        'file': "CENMO1-Anno-2020-PM2.5.csv",
        'year': 2020,
        'thresholds': pm25_thresholds,
        'title': "PM 2.5 emissions in 2020"
    }, {
        'file': "CENMO1-Anno-2020-PM10.csv",
        'year': 2020,
        'thresholds': pm10_thresholds,
        'title': "PM 10 emissions in 2020"
    }]
_plot_daily_pollution(monserrato_data, "cenmo1-daily",
                      title='Daily emissions in Monserrato')


cagliari_data = [
    {
        'file': "CENCA1-Anno-2019-PM2.5.csv",
        'year': 2019,
        'thresholds': pm25_thresholds,
        'title': "PM 2.5 emissions 2019"
    }, {
        'file': "CENCA1-Anno-2019-PM10.csv",
        'year': 2019,
        'thresholds': pm10_thresholds,
        'title': "PM 10 emissions in 2019"
    }, {
        'file': "CENCA1-Anno-2020-PM2.5.csv",
        'year': 2020,
        'thresholds': pm25_thresholds,
        'title': "PM 2.5 emissions in 2020"
    }, {
        'file': "CENCA1-Anno-2020-PM10.csv",
        'year': 2020,
        'thresholds': pm10_thresholds,
        'title': "PM 10 emissions in 2020"
    }]
_plot_daily_pollution(cagliari_data, "cenca1-daily",
                      title='Daily emissions in Cagliari')

# Quartu
quartu_data = [
    {
        'file': "CENQU1-Anno-2019-PM10.csv",
        'year': 2019,
        'thresholds': pm10_thresholds,
        'title': "PM 10 emissions in 2019"
    }, {
        'file': "CENQU1-Anno-2020-PM10.csv",
        'year': 2020,
        'thresholds': pm10_thresholds,
        'title': "PM 10 emissions in 2020"
    }]
_plot_daily_pollution(quartu_data, "cenqu1-daily",
                      title="Daily emissions in Quartu Sant'Elena")
