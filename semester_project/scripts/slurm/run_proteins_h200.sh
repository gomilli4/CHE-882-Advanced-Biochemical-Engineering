#!/bin/bash --login
#SBATCH --job-name=alpha_glycans
#SBATCH --partition=gpu
#SBATCH --gpus=h200:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00
#SBATCH --array=0-32%4
#SBATCH --output=logs/af3_%A_%a.out
#SBATCH --error=logs/af3_%A_%a.err
#SBATCH --requeue

set -euo pipefail

module purge
module load AlphaFold3/3.0.1-foss-2023a-CUDA-12.4.0

unset XLA_FLAGS
unset XLA_CLIENT_MEM_FRACTION
unset XLA_PYTHON_CLIENT_MEM_FRACTION
export XLA_PYTHON_CLIENT_PREALLOCATE=false

AF3_MODELS=/mnt/gs21/scratch/gomilli4/af3_weights
AF3_DB=/mnt/research/common-data/alphafold/database_3

mkdir -p logs outputs

JSON_FILE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" job_list.txt)
RUN_BASENAME="${JSON_FILE%.json}"

echo "Job ID: ${SLURM_JOB_ID}"
echo "Task ID: ${SLURM_ARRAY_TASK_ID}"
echo "Host: $(hostname)"
echo "JSON: ${JSON_FILE}"

run_alphafold.py \
  --json_path="json_inputs/${JSON_FILE}" \
  --model_dir="${AF3_MODELS}" \
  --db_dir="${AF3_DB}" \
  --output_dir="outputs/${RUN_BASENAME}"
