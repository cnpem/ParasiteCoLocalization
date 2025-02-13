#!/bin/sh
#SBATCH --job-name=parasite_colocalization
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --partition=short-gpu-small
#SBATCH --gres=gpu:1g.5gb:1
#SBATCH --mem-per-cpu=4G

DATA_DIR=$1
RESULTS_DIR=$2
singularity run --nv /opt/images/cellprofiler/cellprofiler-4_2_6.sif -c -r -p parasitecolocalization_v10.cppipe -i $DATA_DIR -o $RESULTS_DIR --images-per-batch=12
python postprocessing.py $RESULTS_DIR
