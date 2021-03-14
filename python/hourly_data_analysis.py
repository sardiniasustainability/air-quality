# Analyse hourly emission data

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


def _plot_thresholds(thresholds):
    """ Plot horizontal lines with threshold levels
    """
    if "WhoDaily" in thresholds:
        plt.axhline(y=thresholds["WhoDaily"], color='red',
                    linestyle='--', label="WHO daily threshold")
    if "WhoYearly" in thresholds:
        plt.axhline(y=thresholds["WhoYearly"], color='magenta',
                    linestyle='--', label="WHO yearly threshold")
    if "ItaDaily" in thresholds:
        plt.axhline(y=thresholds["ItaDaily"], color='red', linestyle=':',
                    label="Italian daily threshold")
    if "ItaYearly" in thresholds:
        plt.axhline(y=thresholds["ItaYearly"], color='magenta', linestyle=':',
                    label="Italian yearly threshold")


def _plot_daily_pollution(data_file_name, output_file_name, year, thresholds, title=''):
    """ Plot the data about daily pollution
    """
    # Read data
    daily_pollution_data = pd.read_csv(
        "./data/hourly_emissions/" + data_file_name, comment="#")
    daily_pollution_data = _convert_to_timeseries(daily_pollution_data, year)

    # Line plot
    plt.figure()
    ax = daily_pollution_data.plot(label="Daily measurements")
    ax.set_ylabel("Concentration of pollutant (μg/m³)")
    ax.set_xlabel("Date")
    ax.set_title(title)
    plt.axhline(y=daily_pollution_data.mean(), color='black',
                linestyle='-', label="Yearly mean")
    _plot_thresholds(thresholds)
    ax.legend()

    plt.tight_layout()

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

# PM 2.5
_plot_daily_pollution("CENMO1-Anno-2019-PM2.5.csv",
                      "cenmo1-2019-pm25.png", 2019, pm25_thresholds,
                      title="PM 2.5 emissions in Monserrato")
_plot_daily_pollution("CENMO1-Anno-2020-PM2.5.csv",
                      "cenmo1-2020-pm25.png", 2020, pm25_thresholds,
                      title="PM 2.5 emissions in Monserrato")
_plot_daily_pollution("CENCA1-Anno-2019-PM2.5.csv",
                      "cenca1-2019-pm25.png", 2019, pm25_thresholds,
                      title="PM 2.5 emissions in Cagliari")
_plot_daily_pollution("CENCA1-Anno-2020-PM2.5.csv",
                      "cenca1-2020-pm25.png", 2020, pm25_thresholds,
                      title="PM 2.5 emissions in Cagliari")
# PM 10
_plot_daily_pollution("CENMO1-Anno-2019-PM10.csv",
                      "cenmo1-2019-pm10.png", 2019, pm10_thresholds,
                      title="PM 10 emissions in Monserrato")
_plot_daily_pollution("CENMO1-Anno-2020-PM10.csv",
                      "cenmo1-2020-pm10.png", 2020, pm10_thresholds,
                      title="PM 10 emissions in Monserrato")
_plot_daily_pollution("CENCA1-Anno-2019-PM10.csv",
                      "cenca1-2019-pm10.png", 2019, pm10_thresholds,
                      title="PM 10 emissions in Cagliari")
_plot_daily_pollution("CENCA1-Anno-2020-PM10.csv",
                      "cenca1-2020-pm10.png", 2020, pm10_thresholds,
                      title="PM 10 emissions in Cagliari")
_plot_daily_pollution("CENQU1-Anno-2019-PM10.csv",
                      "cenqu1-2019-pm10.png", 2019, pm10_thresholds,
                      title="PM 10 emissions in Quartu Sant'Elena")
_plot_daily_pollution("CENQU1-Anno-2020-PM10.csv",
                      "cenqu1-2020-pm10.png", 2020, pm10_thresholds,
                      title="PM 10 emissions in Quartu Sant'Elena")
