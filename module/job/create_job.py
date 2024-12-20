import os


def create_job(
    name: str,
    env: str,
    script_dir: str = "./job",
    output_dir: str = "./model",
    partition: str = "gpu",
    nodes: int = 1,
    ntasks: int = 1,
    cpus_per_task: int = 4,
    mem: int = 64,
    gpu_type: str = "a40",
    gpus_per_node: int = 1,
    time: int = 120,
) -> None:
    """
    Create a job script for slurm.

    Args:
        name (str): Name of the job.
        env (str): Name of the conda environment.
        script_dir (str): Directory to save the job script relative to main.
        output_dir (str): Directory to save the output relative to main.
        partition (str): Partition to run the job.
        nodes (int): Number of nodes.
        ntasks (int): Number of tasks.
        cpus_per_task (int): Number of CPUs per task.
        mem (int): Memory in GB.
        gpu_type (str): Type of GPU.
        gpus_per_node (int): Number of GPUs per node.
        time (int): Time in minutes.

    Returns:
        None
    """
    name = name.replace(" ", "_")
    os.makedirs(script_dir, exist_ok=True)
    dest_dir = f"{output_dir}/{name}"
    fn = f"{script_dir}/{name}.slurm"

    # arguments
    args = {
        "job-name": name,
        "partition": partition,
        "nodes": nodes,
        "ntasks": ntasks,
        "cpus-per-task": cpus_per_task,
        "mem": f"{mem}G",
        "gres": f"gpu:{gpu_type}:{gpus_per_node}",
        "time": f"{time//60}:{time%60}:00",
        "output": f'$(dirname "$(realpath "$0")")/../logs/{name}_%j.log',
    }

    # commands
    setup = [
        "export GIT_PYTHON_REFRESH=quiet",
        "conda init",
        "source ~/.bashrc",
        f"conda activate {env}",
    ]

    with open(fn, "w") as f:
        f.write("#!/bin/bash\n")
        for key, value in args.items():
            f.write(f"#SBATCH --{key}={value}\n")
        f.write("\n" + "\n".join(setup) + "\n\n")
        f.write(f'python $(dirname "$(realpath "$0")")/../main.py --dest {dest_dir}')
