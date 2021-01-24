# air_quality_helpers.py    Helpers for the notebook

def _select_pollutant(pollution_data, pollutant_name):
    """ Select the rows in the dataframe that refer to the given pollutant
    """
    data_by_pollutant = pollution_data.loc[
        pollution_data['Inquinante'] == pollutant_name]
    return data_by_pollutant


def _associate_geographic_data(pollution_data):
    """ Add geographic data to yearly pollution data for plotting
    """
    import geopandas as gp

    map_data = gp.read_file('./data/geo/comune-limits.shp')
    merged_map = map_data.merge(pollution_data,
                                how="outer",
                                left_on="nome",
                                right_on="Comune")
    return merged_map


def _compose_map_title(economic_activity, pollutant_name):
    """ Given the economic activity, compose the title
    """
    if economic_activity:
        title = economic_activity + ": "
    else:
        title = economic_activity
    title = title + pollutant_name
    return title


def _plot_pollution_map(pollution_data, pollutant_name, economic_activity=''):
    """ Plot pollution data on a map
    """
    import matplotlib.pyplot as plt

    _, ax = plt.subplots(figsize=(10, 7))

    plt.tick_params(left=False,
                    bottom=False,
                    labelleft=False,
                    labelbottom=False)

    pollution_data.plot(column="Valore",
                        cmap='OrRd',
                        ax=ax,
                        linewidth=0.8,
                        edgecolor='0.1',
                        legend=True)

    title = _compose_map_title(economic_activity, pollutant_name)
    ax.set_title(title)


def plot_yearly_pollution_in_map(pollution_data, pollutant_name, economic_activity=''):
    """ Plot pollution data on the map of Sardinia
    """
    data_by_pollutant = _select_pollutant(pollution_data, pollutant_name)
    data_by_pollutant = _associate_geographic_data(data_by_pollutant)
    _plot_pollution_map(data_by_pollutant, pollutant_name, economic_activity)


def _padded_number_to_str(k):
    """ Convert a numbert to a string and pad it with empty spaces
    """
    col_string = str(k)
    col_string = col_string.rjust(4, " ")
    return col_string


def print_metadata(dataframe, message):
    """ Print the metadata of a dataframe
    """
    print(message)
    k = 0
    for col in dataframe.columns:
        col_string = _padded_number_to_str(k)
        print("   " + col_string + ": " + col)
        k = k+1


def pollutants_in_data(pollution_data):
    """ List the pollutants whose data is available
    """
    return pollution_data.Inquinante.unique()


def print_pollutants(pollution_data):
    """ Print a list of the pollutants in the given data
    """
    print("Data available for the following pollutants:")
    available_pollutants = pollutants_in_data(pollution_data)
    k = 0
    for poll in available_pollutants:
        num_pollutant = _padded_number_to_str(k)
        print("   " + num_pollutant + ": " + poll)
        k = k+1
