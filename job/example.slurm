#!/bin/bash
#SBATCH --job-name=example
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=64G
#SBATCH --gres=gpu:a40:1
#SBATCH --time=2:0:00
#SBATCH --output=../model/example/example_%j.log

export GIT_PYTHON_REFRESH=quiet
conda init
source ~/.bashrc
conda activate slurm-cnn

python ../main.py --dest ./model/example