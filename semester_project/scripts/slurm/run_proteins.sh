#!/bin/bash --login
#SBATCH --job-name=alpha_glycans_gen2
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --array=0-32%4
#SBATCH --output=logs/af3_%A_%a.out
#SBATCH --error=logs/af3_%A_%a.err

set -euo pipefail

module purge
module load AlphaFold3/3.0.1-foss-2023a-CUDA-12.4.0

export XLA_FLAGS="--xla_disable_hlo_passes=custom-kernel-fusion-rewriter"

AF3_MODELS=/mnt/gs21/scratch/gomilli4/af3_weights
AF3_DB=/mnt/research/common-data/alphafold/database_3

mkdir -p logs outputs

JSON_FILE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" job_list.txt)
RUN_BASENAME="${JSON_FILE%.json}"

run_alphafold.py \
  --json_path="json_inputs/${JSON_FILE}" \
  --model_dir="${AF3_MODELS}" \
  --db_dir="${AF3_DB}" \
  --output_dir="outputs/${RUN_BASENAME}" \
  --flash_attention_implementation=xla
