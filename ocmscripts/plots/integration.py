from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shared

from ocmscripts.config import FIGURES_DIR, REPORTS_DIR


def main():
    """Plot the figure"""
    nrows, ncols = 1, 1
    width, aspect_ratio = 17, 1.7
    integration_dir = Path(REPORTS_DIR / "plots")

    plt.rcParams.update(shared.get_fontsizes(base = 9))
    plt.rcParams.update(
        shared.get_figsizes(
            nrows=nrows,
            ncols=ncols,
            aspect_ratio=aspect_ratio,
            width=width,
            constrained_layout=True,
            tight_layout=True,
        )
    )

    (FIGURES_DIR / 'ti_steps').mkdir(parents=True, exist_ok=True)

    for int_file in integration_dir.glob("plots*"):
        output_path = FIGURES_DIR / 'ti_steps' / (int_file.name + ".pdf")
        file = pd.read_csv(int_file, header=0)

        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(width*shared.CM_TO_INCH, width*shared.CM_TO_INCH/aspect_ratio*nrows))
        ax.errorbar(np.arange(64), -file['accuracy'], yerr=file['std'], marker='.')
        ax.invert_yaxis()
        ax.set_xticks(np.arange(64)[::4], file['β'][::4].round(3))
        ax.set_yticks(ticks=[1000, 1500, 2000, 2500, 3000], labels = np.array([r'$-1.0 \times 10^3$', r'$-1.5 \times 10^3$', r'$-2.0 \times 10^3$', r'$-2.5 \times 10^3$', r'$-3.0 \times 10^3$']))
        ax.set_ylabel(r'$\ln \mathcal{A}_{\mathcal{MC}} (\beta)$')
        ax.set_xlabel(r'Inverse temperature $\beta$')

        suffix = int_file.name.split('base')[1]
        
        if suffix: 
            math_suffix = suffix.replace("_", r" \rightarrow ")
            math_suffix = math_suffix.strip()
            if math_suffix.startswith(r"\rightarrow"):
                math_suffix = math_suffix[len(r"\rightarrow"):].strip()
            
            fig_title = f'TI for base ${math_suffix}$'
        else:
            fig_title = 'TI for base'
        
        fig.suptitle(fig_title)  
        fig.savefig(output_path)


if __name__ == "__main__":
    main()



