import argparse

import matplotlib.pyplot as plt
import nibabel as nib
from matplotlib.widgets import Button, Slider

AXES = {
    "sagittale": 0,
    "coronale": 1,
    "axiale": 2,
}



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Chemin vers un fichier .nii ou .nii.gz")
    parser.add_argument(
        "--vue",
        choices=AXES,
        default="axiale",
        help="Vue à afficher au départ (défaut : axiale)",
    )
    parser.add_argument("--MIP", action="store_true", help="Afficher la projection MIP de l'image (mip si pas mis)")
    args = parser.parse_args()


    print("args.image", args.image)
    print("args.vue", args.vue)
    print("args.MIP", args.MIP)          
    


if __name__ == "__main__":
    main()

#python .\compute_mIP_MIP.py  "..\Data_TP0\Data_TP0\IRM\Brain\t1.nii" --vue axiale