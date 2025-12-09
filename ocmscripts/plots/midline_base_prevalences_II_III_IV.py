"""Compare prevalences in the data with the model predictions."""

from lyscripts.plots import COLORS, BetaPosterior, Histogram, draw
import matplotlib.pyplot as plt
import shared

from ocmscripts.config import FIGURES_DIR, PREVALENCES_DIR


def main():
    """Plot the figure"""

    plot_dict = {'II': {'early': ["000", "002", "004"], 
                        'late': ["001", "003", "005"], 
                        'labels': ["LNL II overall", "LNL II with III", "LNL II without III"],
                        'colors': [COLORS["blue"], COLORS["orange"], COLORS["red"]]
                        }, 
                 'III': {'early': ["006", "008", "010", "012"], 
                        'late': ["007", "009", "011", "013"], 
                        'labels': ["LNL III overall", "LNL III with IV", "LNL III without IV", "LNL III without II"],
                        'colors': [COLORS["blue"], COLORS["orange"], COLORS["red"], COLORS["green"]]
                        }, 
                 'IV': {'early': ["014", "016", "018"], 
                        'late': ["015", "017", "019"], 
                        'labels': ["LNL IV overall", "LNL IV without III", "LNL IV without II"],
                        'colors': [COLORS["blue"], COLORS["green"], COLORS["gray"]], 
                        },
                }

    nrows, ncols = 2, 1
    prevalences_file = PREVALENCES_DIR / "midline_base_midline_scenarios_II_III_IV.hdf5"
    plt.rcParams.update(shared.get_fontsizes(base = 9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            aspect_ratio=4.0,
            width=17,
            constrained_layout=True,
            tight_layout=True,
        )
    )

    for lnl in ['II', 'III', 'IV']:
        output_path = FIGURES_DIR / f"midline_base_prevalences_LNL{lnl}.pdf"
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(17*shared.CM_TO_INCH, 17*shared.CM_TO_INCH/4.0*nrows))
        fig.suptitle(f"Observed vs. predicted prevalences related to LNL {lnl} (midline, base)", fontweight='bold')

        for i, tstage in enumerate(['early', 'late']):
            axes[i].set_ylabel(f"{tstage} T-category", fontweight='bold')
            content = []

            for data, color, label in zip(plot_dict[lnl][tstage], plot_dict[lnl]['colors'], plot_dict[lnl]['labels']):
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
            #draw(axes[i], contents=content, xlims=(0, 45), hist_kwargs = {'bins': 60})
            draw(axes[i], contents=content)
            axes[i].legend(ncols = len(plot_dict[lnl]['labels']))   
            axes[i].set_yticks([])
        
        if lnl == 'IV':
            axes[-1].set_ylim(0, 1.0)
        
        axes[0].set_xticks([])
        axes[-1].set_xlabel('prevalence [%]')
        
        # Manual spacing since we disabled automatic layout
        plt.subplots_adjust(hspace=0.1)
        plt.savefig(output_path, bbox_inches="tight")


if __name__ == "__main__":
    main()