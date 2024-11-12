import os

import pandas
import plotly.express as px


# Function to convert well name
def _convert_well_name(well):
    return chr(64 + int(well[:-3])) + str(int(well[-3:]))


def summarize(
    results_directory: str, image_filepath: str, cell_filepath: str
) -> pandas.DataFrame:
    """
    Summarize the results of sthe parasite co-localization analysis. The
    function reads the results of the image and cell analysis and generates a
    summary table with the following:
    - Total number of cells
    - Total number of spots
    - Number of infected cells
    - Infection rate
    - Median number of spots per infected cell

    The summary table is saved in the results directory as a CSV file.

    Parameters
    ----------
    results_directory : str
        Path to the directory where the results are stored.
    image_filepath : str
        Path to the CSV file with the results of the image object.
    cell_filepath : str
        Path to the CSV file with the results of the cell object.

    Returns
    -------
    pandas.DataFrame
        Summary table with the results of the parasite co-localization
        analysis.
    """
    # Read CSV files
    image_data = pandas.read_csv(image_filepath)
    cell_data = pandas.read_csv(cell_filepath)

    # Process image data
    image_data["WellName"] = (
        image_data["Metadata_Well"].astype(str).apply(_convert_well_name)
    )
    image_data = image_data[["WellName", "Count_Nuclei", "Count_Spots"]]
    image_data.columns = ["WellName", "TotalCells", "TotalSpots"]

    # Process cell data
    cell_data["WellName"] = (
        cell_data["Metadata_Well"].astype(str).apply(_convert_well_name)
    )
    cell_data["InfectedCells"] = (cell_data["Children_Spots_Count"] > 3).astype(int)
    cell_data = cell_data[["WellName", "Children_Spots_Count", "InfectedCells"]]
    cell_data.columns = ["WellName", "TotalSpots", "InfectedCells"]

    # Prepare the summary data frame
    summary = image_data.groupby("WellName").agg(
        {"TotalCells": "sum", "TotalSpots": "sum"}
    )
    infected_summary = cell_data.groupby("WellName").agg({"InfectedCells": "sum"})
    summary = summary.join(infected_summary)

    # Calculate additional metrics
    summary["InfectionRate"] = (summary["InfectedCells"] / summary["TotalCells"]) * 100
    summary["MedianSpotsPerInfectedCell"] = (
        cell_data[cell_data["InfectedCells"] == 1]
        .groupby("WellName")["TotalSpots"]
        .median()
    )

    # Define the well order
    well_order = [f"{row}{col}" for row in "ABCDEFGHIJKLMNOP" for col in range(1, 25)]

    # Convert Metadata_Well to a categorical type with the specified order
    summary.index = pandas.Categorical(
        summary.index, categories=well_order, ordered=True
    )

    # Sort the summary by Metadata_Well
    summary = summary.sort_index()

    # Save summary
    summary.to_csv(os.path.join(results_directory, "summary.csv"))

    return summary


def _plot_plate_map(
    summary: pandas.DataFrame, column: str, title: str, output_filepath: str
) -> None:
    """
    Plot a plate map with the values of a given column.

    Parameters
    ----------
    summary : pandas.DataFrame
        Summary table with the results of the analysis.
    column : str
        Name of the column to plot.
    title : str
        Title of the plot.
    output_filepath : str
        Path to the output file.
    """
    # Split the index into two separate columns
    summary["Row"] = summary.index.str[0]
    summary["Column"] = summary.index.str[1:].astype(int)

    # Create a plate map
    plate_map = summary.pivot(index="Row", columns="Column", values=column)

    # Plot the plate map for the given column
    fig = px.imshow(
        plate_map,
        labels=dict(color=column),
        color_continuous_scale="thermal",
        aspect="equal",
        height=800,
        width=1200,
        text_auto=".1f",
        range_color=[0, round(plate_map.max().max(), -2)],
    )

    # Update the layout
    fig.update(
        layout=dict(
            title={"text": f"{title}", "x": 0.5},
            xaxis=dict(
                title=None,
                tickvals=list(range(1, 25)),
                tickangle=0,
                side="top",
            ),
            yaxis=dict(title=None, autorange="reversed"),
            coloraxis_colorbar=dict(
                title=title,
                ticks="outside",
                yanchor="top",
                y=1,
                thicknessmode="pixels",
                thickness=50,
                outlinewidth=1,  # Add border line to colorbar
                outlinecolor="black",  # Set border color
            ),
        ),
        data=[{"customdata": summary.index.values.reshape(plate_map.shape)}],
    )

    # Update the hover template
    fig.update_traces(
        hovertemplate="Well: %{customdata}<br>"
        + f"{title}"
        + ": %{z:.1f}<extra></extra>"
    )

    # Save the plot to a HTML file
    fig.write_html(output_filepath)


def _plot_scatter_plot(
    summary: pandas.DataFrame, x: str, y: str, title: str, output_filepath: str
) -> None:
    """
    Plot a scatter plot of the results from both software tools.

    Parameters
    ----------
    summary : pandas.DataFrame
        Summary table with the results of the analysis.
    x : str
        Name of the column for the x-axis.
    y : str
        Name of the column for the y-axis.
    title : str
        Title of the plot.
    output_filepath : str
        Path to the output file.
    """
    # Create the scatter plot
    fig = px.scatter(
        summary,
        x=x,
        y=y,
        labels={x: title.split(" vs. ")[1], y: title.split(" vs. ")[0]},
        hover_name=summary.index,
        hover_data={x: ":.1f", y: ":.1f"},
        marginal_x="histogram",
        marginal_y="histogram",
        trendline="ols",
        height=1200,
        width=1200,
    )

    # Update the layout
    fig.update(
        layout=dict(
            title={"text": f"{title}", "x": 0.5},
        )
    )

    # Save the plot to a HTML file
    fig.write_html(output_filepath)


def run(results_directory: str, image_filepath: str, cell_filepath: str) -> None:
    """
    Run the post-processing analysis on the results of the parasite
    co-localization analysis.

    Parameters
    ----------
    results_directory : str
        Path to the directory where the results are stored.
    image_filepath : str
        Path to the CSV file with the results of the image object.
    cell_filepath : str
        Path to the CSV file with the results of the cell object.
    """
    # Summarize the results
    summary = summarize(results_directory, image_filepath, cell_filepath)

    # Create the plate_map directory
    os.makedirs(os.path.join(results_directory, "plate_map"), exist_ok=True)

    # Plot plate map with number of cells
    _plot_plate_map(
        summary=summary,
        column="TotalCells",
        title="Number of Cells",
        output_filepath="results/plate_map/number_of_cells.html",
    )

    # Plot plate map with number of spots
    _plot_plate_map(
        summary=summary,
        column="TotalSpots",
        title="Number of Spots",
        output_filepath="results/plate_map/number_of_spots.html",
    )

    # Plot plate map with infection rate
    _plot_plate_map(
        summary=summary,
        column="InfectionRate",
        title="Infection Rate (%)",
        output_filepath="results/plate_map/infection_rate.html",
    )

    # Plot plate map with median spots per infected cell
    _plot_plate_map(
        summary=summary,
        column="MedianSpotsPerInfectedCell",
        title="Median Spots per Infected Cell",
        output_filepath="results/plate_map/median_spots_per_infected_cell.html",
    )


    # Create the scatter directory
    os.makedirs(os.path.join(results_directory, "scatter"), exist_ok=True)

    # Plot scatter plot for number of infected cells vs number of cells
    _plot_scatter_plot(
        summary=summary,
        x="TotalCells",
        y="InfectedCells",
        title="Number of Infected Cells vs. Number of Cells",
        output_filepath="results/scatter/number_of_cells_vs_number_of_infected_cells.html",
    )

    # Plot scatter plot for infection rate vs number of cells
    _plot_scatter_plot(
        summary=summary,
        x="TotalCells",
        y="InfectionRate",
        title="Infection Rate (%) vs. Number of Cells",
        output_filepath="results/scatter/number_of_cells_vs_infection_rate.html",
    )

    # Plot scatter plot for median spots per infected cell vs number of cells
    _plot_scatter_plot(
        summary=summary,
        x="TotalCells",
        y="MedianSpotsPerInfectedCell",
        title="Median Spots per Infected Cell vs. Number of Cells",
        output_filepath="results/scatter/median_spots_per_infected_cell_vs_number_of_cells.html",
    )

    # Plot scatter plot for median spots per infected cell vs infection rate
    _plot_scatter_plot(
        summary=summary,
        x="InfectionRate",
        y="MedianSpotsPerInfectedCell",
        title="Median Spots per Infected Cell vs. Infection Rate (%)",
        output_filepath="results/scatter/median_spots_per_infected_cell_vs_infection_rate.html",
    )


if __name__ == "__main__":
    run("results", "results/Image.csv", "results/Cell.csv")
