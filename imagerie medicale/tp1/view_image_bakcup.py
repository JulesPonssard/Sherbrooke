import argparse

import matplotlib.pyplot as plt
import nibabel as nib
from matplotlib.widgets import Button, Slider


AXES = {
    "sagittale": 0,
    "coronale": 1,
    "axiale": 2,
}


def extraire_coupe(volume, axe, indice):
    if axe == 0:
        return volume[indice, :, :]
    if axe == 1:
        return volume[:, indice, :]
    return volume[:, :, indice]


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

    volume = nib.load(args.image).get_fdata()
    if volume.ndim != 3:
        parser.error("Ce viewer attend un volume 3D.")

    figure = plt.figure(figsize=(12, 6))
    indices = {nom: volume.shape[axe] // 2 for nom, axe in AXES.items()}
    widgets = []  # Garder les curseurs et boutons actifs.

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
            affichage.set_data(extraire_coupe(volume, axe, indices[nom]).T)
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

    afficher_vue_unique(args.vue)
    plt.show()


if __name__ == "__main__":
    main()
