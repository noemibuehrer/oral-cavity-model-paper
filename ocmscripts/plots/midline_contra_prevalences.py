"""Compare prevalences in the data with the model predictions."""

from lyscripts.plots import COLORS, BetaPosterior, Histogram, draw
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from tomlkit import key
import shared

from ocmscripts.config import FIGURES_DIR, PREVALENCES_DIR

plot_dict = {
    "lat": {"early": ["000", "004", "008", "012", "016"],
            "late": ["001", "005", "009", "013", "017"]},
    "midext": {"early": ["002", "006", "010", "014", "018"],
               "late": ["003", "007", "011", "015", "019"]},
}
plot_colors = [COLORS["blue"], COLORS["orange"], COLORS["green"], COLORS["red"], COLORS["gray"]]
labels = ['LNL I', 'LNL II', 'LNL III', 'LNL IV', 'LNL V']
xmax = [30, 15]
bins = [60, 35]

def main():
    """Plot the figure"""
    
    nrows, ncols = 2, 2
    prevalences_file = PREVALENCES_DIR / "midline_II_I_III_V.hdf5"
    plt.rcParams.update(shared.get_fontsizes(base = 9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            aspect_ratio=1.6,
            width=17,
            constrained_layout=True,
            tight_layout=True,
        )
    )

    output_path = FIGURES_DIR / f"midline_contra_prevalences.pdf"
    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex='col')
    fig.suptitle("Observed vs. predicted prevalence of contralateral involvement", fontweight='bold')

    for i, t_stage in enumerate(["early", "late"]):
        axes[i, 0].set_ylabel(f"{t_stage} T-category", fontweight='bold')
        for j, midext in enumerate(["midext", "lat"]):
            axes[0, j].set_title('Mid. ext.' if midext == 'midext' else 'Lateralised', fontweight='bold')
            axes[1, j].set_xlabel("prevalence [%]")
            content = []
            for data, color, label in zip(plot_dict[midext][t_stage], plot_colors, labels):
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
            draw(axes[i, j], contents=content, xlims=(0, xmax[j]), hist_kwargs = {'bins': bins[j]})
            axes[i, j].legend(ncols = 2)
            axes[i, j].set_yticks([])
    
    for ax in axes.flatten():
        handles, legend_labels = ax.get_legend_handles_labels()

        blank = Line2D([], [], linestyle="none", marker=None, linewidth=0)
        handles2 = handles[:6] + handles[6:] + [blank, blank]
        labels2  = legend_labels[:6]  + legend_labels[6:] + ["", ""]

        ax.legend(handles2, labels2, ncol=2)


    plt.savefig(output_path, bbox_inches="tight")


if __name__ == "__main__":
    main()
        
        