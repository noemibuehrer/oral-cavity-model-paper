"""Compare prevalences in the data with the model predictions."""

from lyscripts.plots import COLORS, BetaPosterior, Histogram, draw
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from tomlkit import key
import shared

from ocmscripts.config import FIGURES_DIR, PREVALENCES_DIR

labels = ["early; lateral", "late; lateral", "early; mid-ext.", "late; mid-ext."]
plot_dict = {
    'I': ["000", "001", "002", "003"],
    'II': ["004", "005", "006", "007"],
    "III": ["008", "009", "010", "011"],
}
plot_colors = [COLORS["blue"], COLORS["orange"], COLORS["green"], COLORS["red"], COLORS["gray"]]
xmax = [30, 15]
bins = [60, 35]

def main():
    """Plot the figure"""
    
    nrows, ncols = 3, 1
    prevalences_file = PREVALENCES_DIR / "midline+II_I+III_V_contra.hdf5"
    plt.rcParams.update(shared.get_fontsizes(base = 9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            aspect_ratio=1.7,
            width=17,
            constrained_layout=True,
            tight_layout=True,
        )
    )

    output_path = FIGURES_DIR / f"midline_contra_prevalences.pdf"
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex='col', figsize=(17*shared.CM_TO_INCH, 17*shared.CM_TO_INCH/3.5*nrows))
    fig.suptitle("Observed vs. predicted prevalence of involvement\nin contralateral LNLs I, II and III", fontweight='bold')

    for i, lnl in enumerate(plot_dict.keys()):
        axes[i].set_ylabel(f"contra LNL {lnl}", fontweight='bold')
        content = []
        for data, color, label in zip(plot_dict[lnl], plot_colors, labels):
            content.append(
                Histogram.from_hdf5(
                    filename = prevalences_file,
                    dataname = data,
                    color = color,
                    label = label,
                )
            )
            content.append(
                BetaPosterior.from_hdf5(
                    filename = prevalences_file,
                    dataname = data,
                    color = color,
                )
            )
        draw(axes[i], contents=content, xlims = (0, 30))
        axes[i].legend(ncols=4)
        axes[i].set_yticks([])

    plt.savefig(output_path, bbox_inches="tight")


if __name__ == "__main__":
    main()
        
        