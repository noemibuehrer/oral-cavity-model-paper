"""Compare prevalences in the data with the model predictions."""

from lyscripts.plots import COLORS, BetaPosterior, Histogram, draw
import matplotlib.pyplot as plt
import shared

from ocmscripts.config import FIGURES_DIR, PREVALENCES_DIR

SCENARIO_CONFIGS = {
    'lnl_I': {
        'title': "Base and winning graph's prevalence predictions",
        'output_file': "midline_II_I_IV_V_vs_base_I.pdf",
        'xlim': 55,
        'bins': 60,
        'groups': {
            '1': {
                'early': ["000", "004"], 
                'late': ["001", "005"], 
                'labels': ["LNL I overall", "LNL I without II"],
                'colors': [COLORS["blue"], COLORS["green"]]
            },
            '2': {
                'early': ["002", "006"], 
                'late': ["003", "007"], 
                'labels': ["LNL I with II", "LNL II without I"],
                'colors': [COLORS["orange"], COLORS["red"]]
            },
        }
    },
    'lnl_V': {
        'title': "Base and winning graph's prevalence predictions", 
        'output_file': "midline_II_I_IV_V_vs_base_V.pdf",
        'xlim': 10,
        'bins': 30,
        'groups': {
            '1': {
                'early': ["020", "018"], 
                'late': ["021", "019"], 
                'labels': ["LNL V without IV", "LNL V with IV"],
                'colors': [COLORS["red"], COLORS["green"]],
            },
            '2': {
                'early': ["012", "010"], 
                'late': ["013", "011"], 
                'labels': ["LNL V without III", "LNL V with III"],
                'colors': [COLORS["blue"], COLORS["orange"]],
            },
            '3': {
                'early': ["016", "014"], 
                'late': ["017", "015"], 
                'labels': ["LNL V without II", "LNL V with II"],
                'colors': [COLORS["red"], COLORS["blue"]]
            },
        }
    }
}

def plot_lnl_comparison(config_name: str, config: dict):
    """Plot comparison for a single LNL configuration."""
    nrows, ncols = 2, len(config['groups'])
    
    fig, axes = plt.subplots(
        nrows=nrows, ncols=ncols, 
        figsize=(17*shared.CM_TO_INCH, 17*shared.CM_TO_INCH/4.0*nrows)
    )
    fig.suptitle(config['title'], fontweight='bold')
    
    prevalences_base = PREVALENCES_DIR / "midline_base_midline_scenarios_I_V.hdf5"
    prevalences_winning = PREVALENCES_DIR / "midline+II_I+IV_V_midline_scenarios_I_V.hdf5"
    
    for j, (group_id, group_config) in enumerate(config['groups'].items()):
        for i, tstage in enumerate(['early', 'late']):
            if ncols == 1:
                ax = axes[i]
                ax.set_ylabel(f"{tstage} T-category", fontweight='bold')
            else:
                ax = axes[i, j]
                axes[i, 0].set_ylabel(f"{tstage} T-category", fontweight='bold')
                
            #ax.set_ylabel(f"{tstage} T-category", fontweight='bold')
            content = []

            for data, color, label in zip(
                group_config[tstage], 
                group_config['colors'], 
                group_config['labels']
            ):
                content.extend([
                    Histogram.from_hdf5(
                        filename=prevalences_winning,
                        dataname=data,
                        color=color,
                        label=label,
                        zorder=1,
                    ),
                    Histogram.from_hdf5(
                        filename=prevalences_base,
                        dataname=data,
                        color=color,
                        label='base graph',
                        histtype='step',
                        linewidth=1.5,
                        hatch=r"\\\\",
                        zorder=2,
                    ),
                    BetaPosterior.from_hdf5(
                        filename=prevalences_base,
                        dataname=data,
                        color=color,
                        zorder=3,
                    )
                ])
            
            draw(ax, contents=content, xlims=(0, config['xlim']), 
                 hist_kwargs={'bins': config['bins']})
            ax.legend(loc='upper right')
            ax.set_yticks([])

        if ncols == 1:
            axes[0].set_xticks([])
            axes[-1].set_xlabel('prevalence [%]')
        else:
            axes[0, j].set_xticks([])
            axes[-1, j].set_xlabel('prevalence [%]')
    
    output_path = FIGURES_DIR / config['output_file']
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

def main():
    """Plot all figures"""
    plt.rcParams.update(shared.get_fontsizes(base=9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=2,
            ncols=3,  # max cols
            aspect_ratio=4.0,
            width=17,
            constrained_layout=True,
            tight_layout=True,
        )
    )
    
    for config_name, config in SCENARIO_CONFIGS.items():
        plot_lnl_comparison(config_name, config)

if __name__ == "__main__":
    main()