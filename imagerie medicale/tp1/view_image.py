import argparse

import matplotlib.pyplot as plt
import nibabel as nib
from matplotlib.widgets import Button, Slider


AXES = {
    "sagittale": 0,
    "coronale": 1,
    "axiale": 2,
}


def charger_image(chemin):
    """Charge un NIfTI et renvoie ses données et la taille de ses pixels."""
    image_nifti = nib.load(chemin)

    # Pour un volume, place les axes dans l'orientation canonique RAS+.
    if len(image_nifti.shape) >= 3:
        image_nifti = nib.as_closest_canonical(image_nifti)

    donnees = image_nifti.get_fdata()
    tailles_voxels = image_nifti.header.get_zooms()

    if donnees.ndim == 4:
        # Choix pour la 4e dimension : afficher le premier instant/volume.
        donnees = donnees[:, :, :, 0]
        print("Image 4D détectée : affichage du premier volume (indice 0).")
    elif donnees.ndim not in (2, 3):
        raise ValueError(
            f"L'image possède {donnees.ndim} dimensions; seules les images "
            "NIfTI 2D, 3D et 4D sont acceptées."
        )

    return donnees, tailles_voxels


def extraire_coupe(volume, axe, indice):
    if axe == 0:
        return volume[indice, :, :]
    if axe == 1:
        return volume[:, indice, :]
    return volume[:, :, indice]


def calculer_aspect(tailles_voxels, axe=None):
    """Calcule le rapport physique hauteur/largeur après la transposition."""
    if axe is None:  # Image 2D : dimensions 0 et 1.
        return tailles_voxels[1] / tailles_voxels[0]
    if axe == 0:  # Sagittale : dimensions 1 et 2.
        return tailles_voxels[2] / tailles_voxels[1]
    if axe == 1:  # Coronale : dimensions 0 et 2.
        return tailles_voxels[2] / tailles_voxels[0]
    return tailles_voxels[1] / tailles_voxels[0]  # Axiale : dimensions 0 et 1.


def afficher_image_2d(image, tailles_pixels):
    figure, zone_image = plt.subplots(figsize=(8, 6))
    zone_image.imshow(
        image.T,
        cmap="gray",
        origin="lower",
        aspect=calculer_aspect(tailles_pixels),
    )
    zone_image.set_title("Image NIfTI 2D")
    zone_image.set_xlabel("x")
    zone_image.set_ylabel("y")
    plt.show()


def afficher_volume(volume, tailles_voxels, vue_initiale):
    figure = plt.figure(figsize=(12, 6))
    indices = {nom: volume.shape[axe] // 2 for nom, axe in AXES.items()}
    widgets = []  # Garde les curseurs et boutons actifs.

    def nouveau_mode():
        figure.clear()
        widgets.clear()

    def ajouter_image(nom, position_image, position_curseur):
        axe = AXES[nom]
        zone_image = figure.add_axes(position_image)
        affichage = zone_image.imshow(
            extraire_coupe(volume, axe, indices[nom]).T,
            cmap="gray",
            origin="lower",
            aspect=calculer_aspect(tailles_voxels, axe),
        )
        zone_image.set_title(f"{nom} - coupe {indices[nom]}")

        zone_curseur = figure.add_axes(position_curseur)
        curseur = Slider(
            zone_curseur,
            "Coupe",
            0,
            volume.shape[axe] - 1,
            valinit=indices[nom],
            valstep=1,
        )

        def changer_coupe(valeur):
            indices[nom] = int(valeur)
            nouvelle_coupe = extraire_coupe(volume, axe, indices[nom]).T
            affichage.set_data(nouvelle_coupe)
            zone_image.set_title(f"{nom} - coupe {indices[nom]}")
            figure.canvas.draw_idle()

        curseur.on_changed(changer_coupe)
        widgets.append(curseur)

    def afficher_vue_unique(nom):
        nouveau_mode()
        ajouter_image(nom, [0.1, 0.23, 0.8, 0.7], [0.17, 0.13, 0.55, 0.04])

        zone_bouton = figure.add_axes([0.76, 0.11, 0.18, 0.08])
        bouton = Button(zone_bouton, "Afficher 3 axes")
        bouton.on_clicked(lambda _evenement: afficher_trois_vues())
        widgets.append(bouton)
        figure.canvas.draw_idle()

    def afficher_trois_vues():
        nouveau_mode()
        for colonne, nom in enumerate(AXES):
            gauche = 0.06 + colonne * 0.32
            ajouter_image(
                nom,
                [gauche, 0.28, 0.27, 0.65],
                [gauche + 0.02, 0.17, 0.22, 0.04],
            )

            zone_bouton = figure.add_axes([gauche + 0.05, 0.04, 0.17, 0.07])
            bouton = Button(zone_bouton, f"Détail {nom}")
            bouton.on_clicked(
                lambda _evenement, nom=nom: afficher_vue_unique(nom)
            )
            widgets.append(bouton)

        figure.canvas.draw_idle()

    afficher_vue_unique(vue_initiale)
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image", help="Chemin vers un fichier .nii ou .nii.gz")
    parser.add_argument(
        "--vue",
        choices=AXES,
        default="axiale",
        help="Vue à afficher au départ (défaut : axiale)",
    )
    args = parser.parse_args()

    try:
        donnees, tailles_voxels = charger_image(args.image)
    except (FileNotFoundError, OSError, ValueError) as erreur:
        parser.error(str(erreur))

    if donnees.ndim == 2:
        afficher_image_2d(donnees, tailles_voxels)
    else:
        afficher_volume(donnees, tailles_voxels, args.vue)


if __name__ == "__main__":
    main()
