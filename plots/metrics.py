import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yaml

metrics_dict = {
        "TPR": "True Positive Rate",
        "FPR": "False Positve Rate",
        "TNR": "True Negative Rate",
        "FNR": "False Negative Rate",
        "PPV": "Positive Predictive Value",
        "ACC": "Accuracy",
        "BA": "Balanced Accuracy"
    }


def color_shades(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def metrics_bar_plot(
        cleaner,
        size,
        color,
        width=0.15
    ):

    data = pd.read_csv(f'plots/data/metrics/metrics_{cleaner}_MST_MST_NectarCam.csv')
    unique_ids = data['unique_file_id']
    data = data.drop(columns=["unique_file_id", "tp", "tn", "fp", "fn"])
    labels = [metrics_dict[k] for k in data.keys()]
    x_ticks = np.arange(len(labels))

    interval = np.linspace(-len(data)/2, len(data)/2, len(data))
    print(interval)

    fig, ax = plt.subplots(1, 1, figsize=(size[0]*2, size[1]))
    for idx, alpha in zip(range(len(data)), np.linspace(0.3, 1.0, len(data))):
        ax.bar(x_ticks + interval[idx]*width, data.iloc[idx], width, color=color, alpha=alpha, label=unique_ids[idx])

    ax.set_xticks(x_ticks)
    ax.set_xticklabels(data.keys(), fontsize=8)
    ax.set_ylim(0, 1.05)

    ax.axhline(1.0, ls="dotted", alpha=0.4)
    ax.legend(loc='upper right')

    # ax.set_title(rf'\gls{{mst}} Metrics', fontsize=12)

    plt.savefig(f"plots/metrics_{cleaner}.pdf", bbox_inches='tight', dpi=300)
    plt.close()


if __name__ == "__main__":

    size = plt.gcf().get_size_inches()

    metrics_bar_plot("tailcuts", size=size, color='C0')
    metrics_bar_plot("mars", size=size, color='C1')
    metrics_bar_plot("fact", size=size, color='C2')
    metrics_bar_plot("tcc", size=size, color='C3')

    with open('configs/tailcuts/tailcuts_clean_mst_6.200_4.650_mn_2_config.yml') as f:
        my_dict = yaml.safe_load(f)

    settings = {
        'picture_thresh': my_dict['ImageProcessor']['TailcutsImageCleaner']['picture_threshold_pe'][0][2],
        'boundary_thresh': my_dict['ImageProcessor']['TailcutsImageCleaner']['boundary_threshold_pe'][0][2],
        'min_picture_neighbors': my_dict['ImageProcessor']['TailcutsImageCleaner']['min_picture_neighbors'],
    }

    # print(settings.values())

