import subprocess as sp
from pathlib import Path
from argparse import ArgumentParser

import pandas as pd


parser = ArgumentParser()

parser.add_argument('--username',
                    type=str,
                    help="Username for the ssh server."
)
parser.add_argument('--hostname',
                    default='vollmond',
                    nargs='?',
                    type=str,
                    choices=['vollmond', 'phobos'],
                    help="Hostname for the ssh server. Default: '%(default)s'."
)

parser.add_argument('--tel_type',
                    default='mst',
                    nargs='?',
                    type=str,
                    choices=['mst', 'lst'],
                    help="Telescope type. Default: '%(default)s'."
)

parser.add_argument('--mode',
                    default='angres',
                    nargs='?',
                    type=str,
                    choices=['angres', 'quantiles', 'metrics'],
                    help="Telescope type. Default: '%(default)s'."
)


def downloader(
    username: str,
    hostname: str,
    file_id: int,
    cleaner: str,
    tel_type: str
):
    """
    Download the data from the ssh host server.
    """
    if cleaner == "tail":
        cleaner = "tailcuts"

    if tel_type == "mst":
        dl1_out = Path("./plots/data/mst")
        processed_base = Path(f"/cephfs/users/{username}/Prod5/processed_data/{cleaner}/gamma-diffuse/MST_MST_NectarCam")
        processed_out = Path(f"./plots/data/processed/MST_MST_NectarCam")
        angres_file = f"ang_res_MST_MST_NectarCam_id_{file_id}.csv"
        theta_file = f"theta_MST_MST_NectarCam_id_{file_id}.csv"

    elif tel_type == "lst":
        dl1_out = Path("./plots/data/lst")
        processed_base = Path(f"/cephfs/users/{username}/Prod5/processed_data/{cleaner}/gamma-diffuse/LST_LST_LSTCam")
        processed_out = Path(f"./plots/data/processed/LST_LST_LSTCam")
        angres_file = f"ang_res_LST_LST_LSTCam_id_{file_id}.csv"
        theta_file = f"theta_LST_LST_LSTCam_id_{file_id}.csv"

    angres_out = processed_out / Path("angular_resolution") / cleaner
    theta_out = processed_out / Path("theta") / cleaner

    dl1_out.mkdir(exist_ok=True, parents=True)
    angres_out.mkdir(exist_ok=True, parents=True)
    theta_out.mkdir(exist_ok=True, parents=True)

    angres_out = angres_out / angres_file
    theta_out = theta_out / theta_file

    sp.run([
        "scp",
        f"{username}@{hostname}:{processed_base}/angular_resolution/{angres_file}",
        f"{angres_out}"
    ], check=True)

    sp.run([
        "scp",
         f"{username}@{hostname}:{processed_base}/theta/{theta_file}",
         f"{theta_out}"
    ], check=True)


def download_metrics(
    username: str,
    hostname: str,
    cleaner: str
):
    """
    Download the metrics data.
    """

    if cleaner == "tail":
        cleaner = "tailcuts"

    input_base = Path(
        f"/cephfs/users/{username}/Prod5/processed_data/specific_data/{cleaner}/gamma-diffuse/MST_MST_NectarCam"
    )

    # metrics
    metrics_data = Path("metrics_MST_MST_NectarCam.csv")
    metrics_out = Path("plots/data/metrics")
    metrics_out.mkdir(exist_ok=True, parents=True)
    metrics_out = metrics_out / f"metrics_{cleaner}_MST_MST_NectarCam.csv"

    # survivor data
    survivor_data = Path("survivor_MST_MST_NectarCam.csv")
    survivor_out = Path("plots/data/survivor")
    survivor_out.mkdir(exist_ok=True, parents=True)
    survivor_out = survivor_out / f"survivor_{cleaner}_MST_MST_NectarCam.csv"

    sp.run([
        "scp",
        f"{username}@{hostname}:{input_base}/{metrics_data}",
        f"{metrics_out}"
    ], check=True)

    sp.run([
        "scp",
        f"{username}@{hostname}:{input_base}/{survivor_data}",
        f"{survivor_out}"
    ], check=True)


def quantile_data_dl(
    username: str,
    hostname: str
):
    """
    Download the quantile data.
    """

    quantiles_data = Path("gamma-diffuse_run_980_to_999_dark_cone10_merged.dl1.h5")
    quantiles_out = Path("plots/data/quantiles")
    quantiles_out.mkdir(exist_ok=True, parents=True)
    quantiles_out = quantiles_out / quantiles_data

    sp.run([
        "scp",
        f"{username}@{hostname}:/cephfs/users/{username}/Prod5/merged_data/{quantiles_data}",
        f"{quantiles_out}"
    ], check=True)



if __name__ == "__main__":

    args = parser.parse_args()

    if args.username is None:
        raise ValueError("Please provide a username.")

    if args.hostname is None:
        raise ValueError("Please provide a hostname.")


    combined_table = pd.read_csv("./plots/data/combined_table.csv")

    username = args.username
    hostname = args.hostname
    cleaners = ["tail", "mars", "fact", "tcc"]
    tel_type = args.tel_type

    if args.mode == "angres":
        for cleaner in cleaners:
            for index in combined_table[f"index_{cleaner}"].dropna().astype(int).values:
                print(f"{cleaner}: {index}")
                downloader(username, hostname, index, cleaner, tel_type)

    elif args.mode == "quantiles":
        quantile_data_dl(username, hostname)

    elif args.mode == "metrics":
        for cleaner in cleaners:
            download_metrics(username, hostname, cleaner)


