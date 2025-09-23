"""Compare prevalences in the data with the model predictions."""

import matplotlib.pyplot as plt
import shared

from ocmscripts.config import FIGURES_DIR, PREVALENCES_DIR
from lyscripts.plots import COLORS, BetaPosterior, Histogram, draw

def main():
    """Plot the figure"""

    lnl_I_config = {'1': {'early': ["000", "004"], 
                        'late': ["001", "005"], 
                        'labels': ["LNL I overall", "LNL I without II"],
                        'colors': [COLORS["blue"], COLORS["green"]]
                        },
                    '2': {'early': ["002", "006"], 
                            'late': ["003", "007"], 
                            'labels': ["LNL I with II", "LNL II without I"],
                            'colors': [COLORS["orange"], COLORS["red"]]
                        },
                }
    
    lnl_V_config = {'1': {'early': ["020", "018"], 
                        'late': ["021", "019"], 
                        'labels': ["LNL V without IV", "LNL V with IV"],
                        'colors': [COLORS["red"], COLORS["green"]],
                        },
                    '2': {'early': ["012", "010"], 
                            'late': ["013", "011"], 
                            'labels': ["LNL V without III", "LNL V with III"],
                            'colors': [COLORS["blue"], COLORS["orange"]],

                        },
                    '3': {'early': ["016", "014"], 
                            'late': ["017", "015"], 
                            'labels': ["LNL V without II", "LNL V with II"],
                            'colors': [COLORS["red"], COLORS["blue"]]
                        },
                }
    
    # figure related to LNL I
    nrows, ncols = 2, 2
    prevalences_base = PREVALENCES_DIR / "base_winning_scenarios_integration.hdf5"
    prevalences_winning = PREVALENCES_DIR / "base+II_I+III_V_winning_scenarios_integration.hdf5"
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

    output_path_I = FIGURES_DIR / f"winning_vs_base_I.pdf"
    output_path_V = FIGURES_DIR / f"winning_vs_base_V.pdf"

    for config, output, xmax, bins in zip([lnl_I_config, lnl_V_config], [output_path_I, output_path_V], [55, 10], [60, 30]):
        nrows, ncols = 2, len(config.keys())
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=(17*shared.CM_TO_INCH, 17*shared.CM_TO_INCH/4.0*nrows))
        fig.suptitle(f"Base and winning graph's prevalence predictions", fontweight='bold')
        for j, id in enumerate(config.keys()):
            for i, tstage in enumerate(['early', 'late']):
                axes[i, 0].set_ylabel(f"{tstage} T-category", fontweight='bold')
                content = []

                for data, color, label in zip(config[id][tstage], config[id]['colors'], config[id]['labels']):
                    content.append(
                        Histogram.from_hdf5(
                            filename=prevalences_winning,
                            dataname=data,
                            color=color,
                            label=label,
                            zorder=1,
                        )
                    )
                    content.append(
                        Histogram.from_hdf5(
                            filename=prevalences_base,
                            dataname=data,
                            color=color,
                            label='base graph',
                            histtype='step',
                            linewidth=1.5,
                            hatch=r"\\\\",
                            zorder=2,
                        )
                    )
                    content.append(
                        BetaPosterior.from_hdf5(
                            filename=prevalences_base,
                            dataname=data,
                            color=color,
                            zorder=3,
                        )
                    )
                draw(axes[i, j], contents=content, xlims=(0, xmax), hist_kwargs={'bins': bins})
                axes[i, j].legend(loc='upper right')
                axes[i, j].set_yticks([])

            axes[0, j].set_xticks([])
            axes[-1, j].set_xlabel('prevalence [%]')
            
            plt.savefig(output, bbox_inches="tight")

if __name__ == "__main__":
    main()