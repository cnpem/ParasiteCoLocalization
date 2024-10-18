#!/bin/sh
#SBATCH --job-name=spots_cellprofiler_analysis
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=short-gpu-small
#SBATCH --gres=gpu:1g.5gb:1
#SBATCH --mem-per-cpu=4G


# Processing plate
echo "[==> Processing plate";
singularity run --nv /opt/images/cellprofiler/cellprofiler-4_2_6.sif -c -r -p proj.cpproj
 
# Post-process plate
echo "[==> Post-processing";
python postprocess.py; 


