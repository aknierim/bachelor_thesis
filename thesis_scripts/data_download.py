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

    # dl1_base = Path(f"/cephfs/users/aknierim/Prod5/{cleaner}/{tel_type}/")
    # dl1_file = list(dl1_base.glob(f"*_{file_id}.h5"))[0]
    # print(dl1_file)

    if tel_type == "mst":
        dl1_out = Path("./plots/data/mst")
        processed_base = Path(f"/cephfs/users/aknierim/Prod5/processed_data/{cleaner}/gamma-diffuse/MST_MST_NectarCam")
        processed_out = Path(f"./plots/data/processed/MST_MST_NectarCam")
        angres_file = f"ang_res_MST_MST_NectarCam_id_{file_id}.csv"
        theta_file = f"theta_MST_MST_NectarCam_id_{file_id}.csv"

    elif tel_type == "lst":
        dl1_out = Path("./plots/data/lst")
        processed_base = Path(f"/cephfs/users/aknierim/Prod5/processed_data/{cleaner}/gamma-diffuse/LST_LST_LSTCam")
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

    # sp.run([
    #     f"scp -r {username}@{hostname}:{dl1_file} {dl1_out}/{dl1_file.split('/')[-1]}"
    # ], check=True)

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

    for cleaner in cleaners:
        for index in combined_table[f"index_{cleaner}"].dropna().astype(int).values:
            print(f"{cleaner}: {index}")
            downloader(username, hostname, index, cleaner, tel_type)


