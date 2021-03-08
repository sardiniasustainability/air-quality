# Analyse yearly emission data

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def _select_data(pollution_data, pollutant_name, province_name):
    """ Select the rows in the dataframe that refer to the given pollutant
        and province
    """
    data_by_pollutant = pollution_data.loc[
        (pollution_data['Inquinante'] == pollutant_name) &
        (pollution_data['Provincia'] == province_name)].copy()
    # Delete now-implicit data
    data_by_pollutant.pop('Inquinante')
    data_by_pollutant.pop('Provincia')
    # Rename the "Valore" column
    category = data_by_pollutant.Macrosettore.unique()
    data_by_pollutant.rename(
        columns={'Valore': category[0]}, inplace=True)
    data_by_pollutant.pop('Macrosettore')
    # Clean the "Comune" column
    data_by_pollutant.set_index('Comune')
    data_by_pollutant.Comune = data_by_pollutant.Comune.str.title()
    return data_by_pollutant


def _read_data(file_name, pollutant_name, province_name):
    """ Read the data from the file and select the desired rows
    """
    pollutant_data = pd.read_csv(file_name)
    pollutant_data = _select_data(
        pollutant_data, pollutant_name, province_name)
    return pollutant_data


def _join_multiple(dataframes):
    """ Join multiple tables into one
    """
    from functools import reduce
    joined_tables = reduce(
        lambda left, right: pd.merge(left, right), dataframes)
    return joined_tables


def _plot_data(pollutant, province, file_name):
    """ Read and plot the data for the given pollutant and the given province
    """
    # Read data from the files
    base_path = "./data/yearly_emissions"
    all_data = [_read_data(file_name, pollutant, province)
                for file_name in Path(base_path).glob('*.csv')]
    total_data = _join_multiple(all_data)

    # Plot stacked bar plot
    ax = total_data.plot.barh(stacked=True)
    ax.set_yticklabels(total_data["Comune"])
    ax.set_xlabel(pollutant)
    ax.set_ylabel(total_data.index.name)
    ax.set_title("Concentrazione di particolato nella provincia di Cagliari")
    ax.invert_yaxis()
    ax.legend(bbox_to_anchor=(1, 1), loc="upper left")

    # Resize images
    fig = plt.gcf()
    image_height = 12
    image_width = 9
    image_left_margin = 1.5/image_width
    image_right_margin = 3/image_width
    fig.set_size_inches(image_width, image_height)
    plt.subplots_adjust(left=image_left_margin, right=image_right_margin)
    plt.tight_layout()

    # Save figures
    plt.savefig("./figures/" + file_name, dpi=300)


_plot_data("PM2,5 ( Mg ) ", "CAGLIARI", "pm25.png")
_plot_data("PM10 ( Mg ) ", "CAGLIARI", "pm10.png")


# [markdown]
# ## Hourly emissions
#
# The hourly emissions are obtained by direct reading at measurement stations. The following is a complete list of all the available measurement stations.
#
# | Code          | Province                        | Comune              |
# |---------------|---------------------------------|---------------------|
# | cenas6        | Città Metropolitana di Cagliari | Assemini            |
# | cenas8        | Città Metropolitana di Cagliari | Assemini            |
# | cenas9        | Città Metropolitana di Cagliari | Assemini            |
# | cenca1        | Città Metropolitana di Cagliari | Cagliari            |
# | cenmo1        | Città Metropolitana di Cagliari | Monserrato          |
# | cenqu1        | Città Metropolitana di Cagliari | Quartu Sant'Elena   |
# | censa2        | Città Metropolitana di Cagliari | Sarroch             |
# | censa3        | Città Metropolitana di Cagliari | Sarroch             |
# | cenma1        | Nuoro                           | Macomer             |
# | cennu1        | Nuoro                           | Nuoro               |
# | cennu2        | Nuoro                           | Nuoro               |
# | cenot3        | Nuoro                           | Ottana              |
# | censn1        | Nuoro                           | Siniscola           |
# | cenor1        | Oristano                        | Oristano            |
# | cenor2        | Oristano                        | Oristano            |
# | cesgi1        | Oristano                        | Santa Giusta        |
# | cealg1        | Sassari                         | Alghero             |
# | cenpt1        | Sassari                         | Porto Torres        |
# | cens10        | Sassari                         | Olbia               |
# | cens12        | Sassari                         | Sassari             |
# | cens16        | Sassari                         | Sassari             |
# | censs2        | Sassari                         | Sassari             |
# | censs3        | Sassari                         | Porto Torres        |
# | censs4        | Sassari                         | Porto Torres        |
# | ceolb1        | Sassari                         | Olbia               |
# | cencb2        | Sud Sardegna                    | Carbonia            |
# | cenig1        | Sud Sardegna                    | Iglesias            |
# | cennf1        | Sud Sardegna                    | Gonnesa             |
# | cennm1        | Sud Sardegna                    | Nuraminis           |
# | cenps4        | Sud Sardegna                    | Portoscuso          |
# | cenps6        | Sud Sardegna                    | Portoscuso          |
# | cenps7        | Sud Sardegna                    | Portoscuso          |
# | cense0        | Sud Sardegna                    | Seulo               |
# | censg3        | Sud Sardegna                    | San Gavino Monreale |

# Let's focus on the Sarroch station _censa2_, in particular the CO emissions:


# daily_pollution_data = pd.read_csv(
#     "../data/hourly_emissions_sarroch/censa2-sarroch-co-2020.csv", comment="#")
# data_to_plot = h.convert_to_timeseries(daily_pollution_data)
# h.plot_daily_pollution(data_to_plot, "CO emissions in Sarroch (CA) [mg/m^3]")
#
