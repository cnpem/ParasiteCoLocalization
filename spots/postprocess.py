import pandas as pd


# Function to convert well name
def convert_well_name(well):
    return chr(64 + int(well[:-3])) + str(int(well[-3:]))


# Read the CSV files
image_data = pd.read_csv("./results/Image.csv")
cell_data = pd.read_csv("./results/Cell.csv")

# Process image data
image_data["WellName"] = (
    image_data["Metadata_Well"].astype(str).apply(convert_well_name)
)
image_data = image_data[["WellName", "Count_Nuclei", "Count_Spots"]]
image_data.columns = ["WellName", "TotalCells", "TotalSpots"]

# Process cell data
cell_data["WellName"] = cell_data["Metadata_Well"].astype(str).apply(convert_well_name)
cell_data["InfectedCells"] = (cell_data["Children_Spots_Count"] > 3).astype(int)
cell_data = cell_data[["WellName", "Children_Spots_Count", "InfectedCells"]]
cell_data.columns = ["WellName", "TotalSpots", "InfectedCells"]

# Prepare the summary data frame
summary = image_data.groupby("WellName").agg({"TotalCells": "sum", "TotalSpots": "sum"})
infected_summary = cell_data.groupby("WellName").agg({"InfectedCells": "sum"})
summary = summary.join(infected_summary)

# Calculate additional metrics
summary["InfectionRate"] = summary["InfectedCells"] / summary["TotalCells"]
summary["MedianSpotsPerInfectedCell"] = (
    cell_data[cell_data["InfectedCells"] == 1]
    .groupby("WellName")["TotalSpots"]
    .median()
)

# Display the summary
print(summary)
