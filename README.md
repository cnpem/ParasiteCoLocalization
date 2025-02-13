# Parasite Co-localization Assay

This repository contains the source code for analyzing Chagas parasite co-localization in microscopy images.

## Images

The images were generated from a high-content screening (HCS) assay of embryonic mouse cardiac cells (H9C2 cell line), infected with the amastigote form of *Trypanosoma cruzi* (strain Dm28c). The cells were treated with a library of compounds at different concentrations, using DMSO as a negative control. The cell and parasite nuclei were stained with Hoechst, and the images were acquired using the Operetta HCS (Perkin Elmer) at LNBio.

## Analysis

The images were processed using open-source tools, such as CellProfiler, for image processing analysis, and then data mined in Python for quantitative analysis. The custom CellProfiler pipeline included pre-processing, segmentation of nuclei, cytoplasm, and parasites, and calculation of metrics (number of parasites per cell and number of infected cells).

To run the pipeline, follow these steps:

1. Install [CellProfiler](https://cellprofiler.org/releases/) and the required [plugins](https://github.com/cnpem/lnbio-bioimage-analysis/blob/main/cellprofiler/INSTALLATION.md#cellprofiler-plugins).

2. Run the pipeline and data mining using the `run.sh` script:

```bash
# Running on local machine
bash run.sh -m local -p /path/to/CellProfiler-plugins/active_plugins
```

or

```bash
# Running on HPC marvin machine
sbatch run.sh -m marvin
```

The output will be saved in the `results` directory and will include the following files:

```bash
results/
├── summary.csv # Summary of the number of cells, parasites, infection rate, and median number of parasites per infected cell per well
├── plate_map/
│   ├── number_of_cells.html # Interactive visualization of the number of cells per well
│   ├── number_of_spots.html # Interactive visualization of the number of parasites per well
│   ├── infection_rate.html # Interactive visualization of the infection rate per well
│   ├── number_of_infected_cells.html # Interactive visualization of the number of infected cells per well
│   └── median_spots_per_infected_cell.html # Interactive visualization of the median number of parasites per infected cell per well
└── scatter/
    ├── number_of_infected_cells_vs_number_of_cells.html # Scatter plot comparing the number of cells and infected cells per well
    ├── infection_rate_vs_number_of_cells.html # Scatter plot comparing the number of cells and infection rate per well
    ├── median_spots_per_infected_cell_vs_number_of_cells.html # Scatter plot comparing the number of cells and median number of parasites per infected cell per well
    └── median_spots_per_infected_cell_vs_infection_rate.html # Scatter plot comparing the infection rate and number of infected cells per well
```

### Authors

- [Patrick H. F. Alvares](https://github.com/PatrickHFA)
- [João V. S. Guerra](https://github.com/jvsguerra)
- [José G. C. Pereira](https://github.com/zgcarvalho)

## Benchmarking

The results obtained using the parasite co-localization protocols developed with the open-source software CellProfiler were benchmarked against the reference protocol applied in the proprietary high-content image analysis software, Columbus.

The comparison was performed quantitatively by comparing the scatter plots of the results obtained for each well of the plate, considering the number of cells, the infection rate, and the median number of parasites per infected cell. The results can be accessed through the following links:

- CellProfiler Results: [summary.csv](https://github.com/cnpem/ParasiteCoLocalization/blob/main/benchmarking/CellProfiler/summary.csv)
- Columbus Results: [summary.txt](https://github.com/cnpem/ParasiteCoLocalization/blob/main/benchmarking/Columbus/summary.txt)

To reproduce the benchmarking analysis, run in the `benchmarking` directory:

```bash
python benchmarking.py
```

The output will be saved in the `comparison` directory and will include the following files:

```bash
benchmarking/
└── comparison/
    ├── number_of_cells.html # Scatter plot comparing the number of cells per well
    ├── infection_rate.html # Scatter plot comparing the infection rate per well
    └── median_spots_per_infected_cell.html # Scatter plot comparing the median number of parasites per infected cell per well
```

## License

This software is licensed under the terms of the GNU General Public License version 3 (GPL3) and is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
