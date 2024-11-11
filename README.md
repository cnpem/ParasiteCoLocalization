# Parasite Co-localization

This repository contains the source code for analyzing Chagas parasite co-localization in microscopy images.

## Images

The images were generated from a high-content screening (HCS) assay of embryonic mouse cardiac cells (H9C2 cell line), infected with the amastigote form of *Trypanosoma cruzi* (strain Dm28c). The cells were treated with a library of compounds at different concentrations, using DMSO as a negative control. The cell and parasite nuclei were stained with Hoechst, and the images were acquired using the Operetta HCS (Perkin Elmer) at LNBio.

## Analysis

The images were processed using open-source tools, such as CellProfiler, for image processing analysis, and then data mined in Python for quantitative analysis. The custom CellProfiler pipeline included pre-processing, segmentation of nuclei, cytoplasm, and parasites, and calculation of metrics (number of parasites per cell and number of infected cells).

To run the pipeline, follow the instructions below:

1. Install [CellProfiler](https://cellprofiler.org/releases/) and the required [plugins](https://github.com/cnpem/lnbio-bioimage-analysis/blob/main/cellprofiler/INSTALLATION.md#cellprofiler-plugins).

2. Run the pipeline and data mining using the `run.sh` script:

```bash
# Running on local machine
bash run.sh -m local -p /path/to/CellProfiler-plugins/active_plugins
```

or

```bash
# Running on HPC marvin machine
bash run.sh -m marvin
```

The output will be saved in the `results` directory and will include the following files:

- `summary.csv`: Contains a summary of the number of cells, parasites, infected cells, and the percentage of infected cells per well.
- `visualization/number_of_cells.html`: Interactive visualization of the number of cells per well.
- `visualization/number_of_spots.html`: Interactive visualization of the number of parasites per well.
- `visualization/number_of_infected_cells.html`: Interactive visualization of the number of infected cells per well.
- `visualization/median_spots_per_infected_cell.html`: Interactive visualization of the median number of parasites per infected cell per well.

### Authors

- [Patrick H. F. Alvares](https://github.com/PatrickHFA)
- [João V. S. Guerra](https://github.com/jvsguerra)
- [José G. C. Pereira](https://github.com/zgcarvalho)

## License

This software is licensed under the terms of the GNU General Public License version 3 (GPL3) and is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
