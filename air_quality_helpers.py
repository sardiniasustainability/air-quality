# air_quality_helpers.py    Helpers for the notebook

def print_metadata(dataframe, message):
    """ Print the metadata of a dataframe
    """
    print(message)
    k = 0
    for col in dataframe.columns:
        col_string = str(k)
        col_string = col_string.rjust(4, " ")
        print("   " + col_string + ": " + col)
        k = k+1


def plot_pollutant(pollution_data, pollutant_name):
    import geopandas
    import matplotlib.pyplot as plt

    comune_name = 'Comune'

    map_data = geopandas.read_file('./geo/comune-limits.shp')
    map_data.rename(columns={'nome': comune_name}, inplace=True)

    data_by_pollutant = pollution_data.loc[
        pollution_data['Inquinante'] == pollutant_name]
    print(data_by_pollutant.head())

    map_data.set_index(comune_name)
    data_by_pollutant.set_index(comune_name)
    merged_map = map_data.merge(data_by_pollutant, how="outer")

    column_to_plot = 'Valore'

    fig, ax = plt.subplots(figsize=(10, 7))

    merged_map.plot(
        column=column_to_plot,
        cmap='OrRd',
        ax=ax,
        linewidth=0.8,
        edgecolor='0.1',
        legend=True)

    curr_ylim_bottom, curr_ylim_top = ax.get_ylim()
    ylim_distance = curr_ylim_top - curr_ylim_bottom
    ax.set_ylim([curr_ylim_bottom, curr_ylim_bottom + ylim_distance/2])

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(pollutant_name)

    return fig
