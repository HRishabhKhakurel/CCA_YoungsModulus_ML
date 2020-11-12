#!/bin/bash
#SBATCH -A m3540 
#SBATCH -J ml_youngsmodulus_ada
#SBATCH --mail-user=hrishabh.khakurel@mavs.uta.edu
#SBATCH --mail-type=ALL
#SBATCH -C haswell
#SBATCH -q regular
#SBATCH -N 1
#SBATCH -t 6:00:00 # time to run the job
#SBATCH -o output.o%j

conda activate myenv

python -c "import xgboost as xgb"
echo "imported xgboost"

srun -n 32 python ./hyp_opt_script_ada.py
echo "script completed"

conda deactivate

