"""Compare prevalences in the data with the model predictions."""

from lyscripts.plots import COLORS, BetaPosterior, Histogram, draw
import matplotlib.pyplot as plt
import shared

from ocmscripts.config import FIGURES_DIR, PREVALENCES_DIR

plot_dict = {
    'I': {
        'lat':{
            'early': ["000", "004"],
            'late': ["001", "005"],
        },
        'midext':{
                'early': ["002", "006"],
                'late': ["003", "007"],
        },
        'labels':['contra LNL II involved', 'contra LNL II healthy'],
        'colors':[COLORS['orange'], COLORS['green']], 
    },
    'III': {
        'lat':{
            'early': ["008", "012"],
            'late': ["009", "013"],
        },
        'midext':{
                'early': ["010", "014"],
                'late': ["011", "015"],
        },
        'labels':['contra LNL II involved', 'contra LNL II healthy'],
        'colors':[COLORS['blue'], COLORS['red']], 
    },
}
xmax = [25, 8]
bins = [40, 30]

def main():
    """Plot the figure"""

    nrows, ncols = 2, 2
    prevalences_file = PREVALENCES_DIR / "midline+II_I+III_V_contra_upstream.hdf5"
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

    for lnl in ['I', 'III']:
        output_path = FIGURES_DIR / f"midline_contra_upstream_prevalences_LNL{lnl}.pdf"
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, sharex='col')
        fig.suptitle(f"Observed vs. predicted prevalence of contralateral LNL {lnl} involvement \ndependent on upstream LNL II involvement", fontweight='bold')

        for i, t_stage in enumerate(['early', 'late']):
            axes[i, 0].set_ylabel(f"{t_stage} T-category", fontweight='bold')
            for j, midext in enumerate(['midext', 'lat']):
                axes[0, j].set_title('Mid. ext.' if midext == 'midext' else 'Lateralised', fontweight='bold')
                axes[1, j].set_xlabel("prevalence [%]")
                content = []

                for data, color, label in zip(plot_dict[lnl][midext][t_stage], plot_dict[lnl]['colors'], plot_dict[lnl]['labels']):
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
                draw(
                    contents=content,
                    axes=axes[i, j],
                    xlims=(0, xmax[j]),
                    hist_kwargs = {'bins': bins[j]}
                )
                axes[i, j].legend()
                axes[i, j].set_yticks([])
    
        plt.savefig(output_path, bbox_inches="tight")
                                        

if __name__ == "__main__":
    main()

