import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter, MultipleLocator
from typer import Typer

from ww.commands.crawl.id_parser import id_parser

app = Typer(name="crit")


def plot_crit(
    title: str,
    x,
    y,
    boundary_label: str,
    left_color: str,
    left_region_label: str,
    right_color: str,
    right_region_label: str,
):
    matplotlib.rc("font", family="Microsoft JhengHei")

    with plt.rc_context(
        {
            "text.color": "#f0f0f0",
            "axes.edgecolor": "#f0f0f0",
            "axes.labelcolor": "#f0f0f0",
            "xtick.color": "#f0f0f0",
            "ytick.color": "#f0f0f0",
            "axes.facecolor": "#080c14",
            "figure.facecolor": "#080c14",
        }
    ):
        _, ax = plt.subplots(figsize=(8, 8))
        ax.xaxis.set_major_locator(MultipleLocator(0.5))
        ax.xaxis.set_minor_locator(MultipleLocator(0.1))
        ax.yaxis.set_major_locator(MultipleLocator(0.2))
        ax.yaxis.set_minor_locator(MultipleLocator(0.05))

        ax.tick_params(axis="x", which="major", labelsize=14)
        ax.yaxis.set_minor_formatter(FormatStrFormatter("%.2f"))
        ax.tick_params(axis="y", which="major", labelsize=14)
        ax.tick_params(axis="y", which="minor", labelsize=8)

        # Boundary
        ax.plot(x, y, label=boundary_label, color="#f0f0f0")

        # Right region
        ax.fill_betweenx(
            [0.05, 0.895],
            1.5,
            4,
            color=right_color,
            label=right_region_label,
        )

        # Left region
        ax.fill_between(
            x,
            y,
            0.895,
            where=(y < 0.895),
            color=left_color,
            label=left_region_label,
        )

        # Formatting
        ax.set_xlabel("暴傷", fontsize=14, fontweight="bold")
        ax.set_ylabel("暴擊", fontsize=14, fontweight="bold")
        ax.set_xlim(xmin=1)
        ax.set_ylim(ymin=0, ymax=1.05)
        ax.legend()
        ax.set_title(title, fontsize=16, fontweight="bold")
        # ax.grid(True)
        ax.grid(which="major", linestyle="-", linewidth=0.5, color="#f0f0f0")
        ax.grid(
            which="minor", linestyle="--", linewidth=0.2, alpha=0.5, color="#f0f0f0"
        )
        plt.show()


@app.command()
def rate_gt_rate_and_dmg():
    """
    (rate + 0.063) * (c_dmg + 0.126) + (1 - 0.063 - rate)...(1)
    (rate + 0.105) * c_dmg + (1 - rate - 0.105)...(2)

    (1) - (2)
    = 0.063c_dmg - 0.105c_dmg + 0.126rate + 0.063 * 0.126 - 0.063 + 0.105
    = -0.042c_dmg + 0.126rate + 0.049938

    0 = -0.042c_dmg + 0.126rate + 0.049938
    -0.126y = -0.042x + 0.049938
    y = (0.042 / 0.126)x - 0.049938 / 0.126
    """
    x = np.array([i * 0.01 + 1.5 for i in range(251)])
    y = (0.042 / 0.126) * x - (0.049938 / 0.126)

    plot_crit(
        "10.5%暴擊 vs 6.3%暴擊 + 12.6%暴傷",
        x,
        y,
        "-0.042x + 0.126y + 0.049938 = 0",
        "#29b6f6",
        "10.5%暴擊 < 6.3%暴擊 + 12.6%暴傷",
        "#ff5733",
        "10.5%暴擊 > 6.3%暴擊 + 12.6%暴傷",
    )


@app.command()
def dmg_gt_rate_and_dmg():
    """
    (rate + 0.063) * (c_dmg + 0.126) + (1 - 0.063 - rate)...(1)
    rate * (c_dmg + 0.21) + (1 - rate)...(2)

    (1) - (2)
    = 0.063c_dmg + 0.126rate + 0.063 * 0.126 - 0.063 - 0.21rate
    = 0.063c_dmg - 0.084rate - 0.055062

    0 = 0.063c_dmg - 0.084rate - 0.055062
    0.063x - 0.084y - 0.055062 = 0
    0.084y = 0.063x - 0.055062
    y = (0.063 / 0.084)x - 0.055062 / 0.084
    """
    x = np.array([i * 0.01 + 1.5 for i in range(251)])
    y = 0.75 * x - 0.6555

    plot_crit(
        "21.0%暴傷 vs 6.3%暴擊 + 12.6%暴傷",
        x,
        y,
        "0.063x - 0.084y - 0.055062 = 0",
        "#ff5733",
        "21.0%暴傷 > 6.3%暴擊 + 12.6%暴傷",
        "#29b6f6",
        "21.0%暴傷 < 6.3%暴擊 + 12.6%暴傷",
    )
