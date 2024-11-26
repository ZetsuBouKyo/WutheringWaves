import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from typer import Typer

from ww.commands.crawl.id_parser import id_parser

app = Typer(name="crit")


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
        matplotlib.rc("font", family="Microsoft JhengHei")

        x_vals = np.array([i * 0.01 + 1.5 for i in range(251)])
        y_vals_new = (0.042 / 0.126) * x_vals - (0.049938 / 0.126)

        # Set up the plot with the updated inequality and the rectangular region
        plt.figure(figsize=(8, 8))
        plt.plot(
            x_vals,
            y_vals_new,
            label=r"-0.042x + 0.126y + 0.049938 = 0",
            color="#f0f0f0",
        )

        # Define the rectangular region constraints: 1.5 <= x <= 4, 0 <= y <= 1
        plt.fill_betweenx(
            [0.05, 0.895],
            1.5,
            4,
            color="#ff5733",
            label="10.5%暴擊 > 6.3%暴擊 + 12.6%暴傷",
        )

        plt.fill_between(
            x_vals,
            y_vals_new,
            0.895,
            where=(y_vals_new < 0.895),
            color="#29b6f6",
            label="10.5%暴擊 < 6.3%暴擊 + 12.6%暴傷",
        )

        # Formatting
        plt.xlabel("暴傷")
        plt.ylabel("暴擊")
        plt.axhline(0, color="#f0f0f0", linewidth=0.5)
        plt.axvline(0, color="#f0f0f0", linewidth=0.5)
        plt.xlim(xmin=1)
        plt.ylim(ymin=0, ymax=1.05)
        plt.legend()
        plt.title("10.5%暴擊 vs 6.3%暴擊 + 12.6%暴傷")
        plt.grid(True)
        plt.show()


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
        matplotlib.rc("font", family="Microsoft JhengHei")

        x_vals = np.array([i * 0.01 + 1.5 for i in range(251)])
        y_vals_new = 0.75 * x_vals - 0.6555

        # Set up the plot with the updated inequality and the rectangular region
        plt.figure(figsize=(8, 8))
        plt.plot(
            x_vals,
            y_vals_new,
            label=r"0.063x - 0.084y - 0.055062 = 0",
            color="#f0f0f0",
        )

        # Define the rectangular region constraints: 1.5 <= x <= 4, 0 <= y <= 1
        plt.fill_betweenx(
            [0.05, 0.895],
            1.5,
            4,
            color="#29b6f6",
            label="21.0%暴傷 < 6.3%暴擊 + 12.6%暴傷",
        )

        plt.fill_between(
            x_vals,
            y_vals_new,
            0.895,
            where=(y_vals_new <= 0.895),
            color="#ff5733",
            label="21.0%暴傷 > 6.3%暴擊 + 12.6%暴傷",
        )

        # Formatting
        plt.xlabel("暴傷")
        plt.ylabel("暴擊")
        plt.axhline(0, color="#f0f0f0", linewidth=0.5)
        plt.axvline(0, color="#f0f0f0", linewidth=0.5)
        plt.xlim(xmin=1)
        plt.ylim(ymin=0, ymax=1.05)
        plt.legend()
        plt.title("21.0%暴傷 vs 6.3%暴擊 + 12.6%暴傷")
        plt.grid(True)
        plt.show()
