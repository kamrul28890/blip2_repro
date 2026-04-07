#!/bin/bash
#SBATCH -A gpu
#SBATCH --constraint=J
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=04:00:00
#SBATCH --job-name=blip2-s2-100k
#SBATCH --output=logs/scholar/%x-%j.out

set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$PWD}"
mkdir -p "$REPO_ROOT/logs/scholar"

: "${VENV_PATH:?Set VENV_PATH to the root of your Scholar Python environment before submitting.}"
: "${STAGE1_CKPT:?Set STAGE1_CKPT before submitting this stage-2 job.}"

source "$VENV_PATH/bin/activate"
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"

cd "$REPO_ROOT"
bash blip2_repro/scripts/scholar/run_stage2_student_100k.sh
