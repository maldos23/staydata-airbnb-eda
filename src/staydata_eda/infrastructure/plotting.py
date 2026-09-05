"""Chart strategies and the matplotlib renderer.

Colour choices follow a validated categorical palette: hues are assigned in a
fixed order and only the first three slots are used, which keeps every pair
separable for colour-vision-deficient readers. Charts that compare one measure
across categories use a single hue, because the category is already carried by
the axis labels - colour never encodes rank.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")  # Headless backend: required inside the Docker image.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ..domain import schema
from ..domain.ports import ChartStrategy, FigureRenderer

LOGGER = logging.getLogger(__name__)

# Validated categorical slots (light surface).
SERIES = ("#2a78d6", "#eb6834", "#1baf7a")
SURFACE = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
GRID = "#e4e3df"

_BASE_STYLE = {
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "axes.edgecolor": GRID,
    "axes.labelcolor": TEXT_SECONDARY,
    "axes.titlecolor": TEXT_PRIMARY,
    "axes.grid": True,
    "axes.axisbelow": True,
    "grid.color": GRID,
    "grid.linewidth": 0.8,
    "xtick.color": TEXT_SECONDARY,
    "ytick.color": TEXT_SECONDARY,
    "font.size": 10,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
}


def _style_axes(ax: plt.Axes, title: str, xlabel: str = "", ylabel: str = "") -> None:
    """Apply the shared recessive styling to an axis (DRY helper)."""
    ax.set_title(title, fontsize=12, fontweight="bold", loc="left", pad=12)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


class PriceDistributionChart(ChartStrategy):
    """Distribution of the target, shown in both scales."""

    @property
    def filename(self) -> str:
        return "fig1_price_distribution.png"

    @property
    def title(self) -> str:
        return "Distribución del precio por noche y de log_price"

    def render(self, frame: pd.DataFrame, output_path: str) -> str:
        price = frame[schema.PRICE_USD].dropna()
        upper = float(price.quantile(0.99))
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))

        axes[0].hist(price[price <= upper], bins=60, color=SERIES[0], edgecolor=SURFACE)
        median = float(price.median())
        axes[0].axvline(median, color=TEXT_PRIMARY, linewidth=1.2, linestyle="--")
        axes[0].annotate(
            f"Mediana USD {median:.0f}",
            xy=(median, axes[0].get_ylim()[1] * 0.9),
            xytext=(8, 0),
            textcoords="offset points",
            color=TEXT_PRIMARY,
            fontsize=9,
        )
        _style_axes(
            axes[0],
            "Precio por noche (recortado en el percentil 99)",
            "USD por noche",
            "Anuncios",
        )

        axes[1].hist(frame[schema.TARGET].dropna(), bins=60, color=SERIES[0], edgecolor=SURFACE)
        _style_axes(axes[1], "log_price (variable objetivo)", "log_price", "Anuncios")

        fig.suptitle(self.title, fontsize=13, fontweight="bold", color=TEXT_PRIMARY, x=0.02, ha="left")
        fig.tight_layout(rect=(0, 0, 1, 0.94))
        fig.savefig(output_path)
        plt.close(fig)
        return output_path


class PriceByRoomTypeChart(ChartStrategy):
    """Price dispersion across the three room types."""

    @property
    def filename(self) -> str:
        return "fig2_price_by_room_type.png"

    @property
    def title(self) -> str:
        return "Precio por noche según tipo de espacio (room_type)"

    def render(self, frame: pd.DataFrame, output_path: str) -> str:
        order = frame[schema.ROOM_TYPE].value_counts().index.tolist()
        groups = [frame.loc[frame[schema.ROOM_TYPE] == value, schema.PRICE_USD].dropna() for value in order]

        fig, ax = plt.subplots(figsize=(8, 4.2))
        box = ax.boxplot(
            groups,
            vert=False,
            patch_artist=True,
            showfliers=False,
            widths=0.55,
            medianprops={"color": SURFACE, "linewidth": 2},
        )
        for patch in box["boxes"]:
            patch.set_facecolor(SERIES[0])
            patch.set_edgecolor(SERIES[0])
        for whisker in box["whiskers"] + box["caps"]:
            whisker.set_color(TEXT_SECONDARY)

        ax.set_yticklabels(order)
        ax.set_xscale("log")
        ax.set_xlim(15, 1400)
        ax.set_xticks([25, 50, 100, 200, 400, 800])
        ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
        # Direct labels: the median is the number a host actually cares about.
        for index, values in enumerate(groups, start=1):
            median = float(values.median())
            upper_whisker = float(values.quantile(0.75) + 1.5 * (values.quantile(0.75) - values.quantile(0.25)))
            ax.annotate(
                f"mediana USD {median:.0f}  ·  n={values.size:,}",
                xy=(min(upper_whisker, 1200), index),
                xytext=(10, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=9,
                color=TEXT_PRIMARY,
            )
        _style_axes(ax, self.title, "USD por noche (escala logarítmica)", "")
        fig.savefig(output_path)
        plt.close(fig)
        return output_path


class PriceVsCapacityChart(ChartStrategy):
    """Median price by capacity, split by room type (three series)."""

    @property
    def filename(self) -> str:
        return "fig3_price_vs_accommodates.png"

    @property
    def title(self) -> str:
        return "Precio mediano según capacidad y tipo de espacio"

    #: Groups smaller than this are dropped: their median is too noisy to plot.
    MIN_GROUP_SIZE = 30

    def render(self, frame: pd.DataFrame, output_path: str) -> str:
        subset = frame[frame[schema.ACCOMMODATES] <= 10]
        fig, ax = plt.subplots(figsize=(8.5, 4.4))
        order = ["Entire home/apt", "Private room", "Shared room"]
        for color, room_type in zip(SERIES, order):
            stats = (
                subset[subset[schema.ROOM_TYPE] == room_type]
                .groupby(schema.ACCOMMODATES)[schema.PRICE_USD]
                .agg(["median", "size"])
            )
            grouped = stats.loc[stats["size"] >= self.MIN_GROUP_SIZE, "median"]
            if grouped.empty:
                continue
            ax.plot(grouped.index, grouped.values, color=color, linewidth=2, marker="o", markersize=5, label=room_type)
            # Direct label at the end of each line (relief for low-contrast hues).
            ax.annotate(
                room_type,
                xy=(grouped.index[-1], grouped.values[-1]),
                xytext=(6, 0),
                textcoords="offset points",
                color=TEXT_PRIMARY,
                fontsize=9,
                va="center",
            )
        ax.legend(frameon=False, loc="upper left", fontsize=9)
        ax.set_xlim(0.6, 12.8)
        _style_axes(ax, self.title, "Huéspedes que admite (accommodates)", "Precio mediano (USD)")
        ax.annotate(
            f"Solo se grafican grupos con al menos {self.MIN_GROUP_SIZE} anuncios",
            xy=(0, -0.22),
            xycoords="axes fraction",
            fontsize=8.5,
            color=TEXT_SECONDARY,
        )
        fig.savefig(output_path)
        plt.close(fig)
        return output_path


class PriceByCityChart(ChartStrategy):
    """Median price per city, one measure across six categories."""

    @property
    def filename(self) -> str:
        return "fig4_price_by_city.png"

    @property
    def title(self) -> str:
        return "Precio mediano por ciudad"

    def render(self, frame: pd.DataFrame, output_path: str) -> str:
        grouped = (
            frame.groupby(schema.CITY)[schema.PRICE_USD]
            .agg(["median", "size"])
            .sort_values("median")
        )
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.barh(grouped.index, grouped["median"], color=SERIES[0], height=0.62)
        for bar, (median, size) in zip(bars, grouped.itertuples(index=False)):
            ax.annotate(
                f"USD {median:.0f}  ·  {size:,} anuncios",
                xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                xytext=(6, 0),
                textcoords="offset points",
                va="center",
                fontsize=9,
                color=TEXT_PRIMARY,
            )
        ax.set_xlim(0, grouped["median"].max() * 1.45)
        _style_axes(ax, self.title, "Precio mediano (USD por noche)", "")
        fig.savefig(output_path)
        plt.close(fig)
        return output_path


class MissingValuesChart(ChartStrategy):
    """Share of missing values per column."""

    @property
    def filename(self) -> str:
        return "fig5_missing_values.png"

    @property
    def title(self) -> str:
        return "Valores faltantes por variable (% de registros)"

    def render(self, frame: pd.DataFrame, output_path: str) -> str:
        missing = (frame.isna().mean() * 100).sort_values()
        missing = missing[missing > 0]
        fig, ax = plt.subplots(figsize=(8, 4.2))
        bars = ax.barh(missing.index, missing.values, color=SERIES[0], height=0.62)
        for bar, value in zip(bars, missing.values):
            ax.annotate(
                f"{value:.1f}%",
                xy=(bar.get_width(), bar.get_y() + bar.get_height() / 2),
                xytext=(5, 0),
                textcoords="offset points",
                va="center",
                fontsize=9,
                color=TEXT_PRIMARY,
            )
        ax.set_xlim(0, float(np.max(missing.values)) * 1.25)
        _style_axes(ax, self.title, "% de registros sin dato", "")
        fig.savefig(output_path)
        plt.close(fig)
        return output_path


class MatplotlibFigureRenderer(FigureRenderer):
    """Renders chart strategies to PNG files inside a target directory."""

    def __init__(self, output_dir: Path) -> None:
        self._output_dir = Path(output_dir)

    def render_all(self, frame: pd.DataFrame, charts: Sequence[ChartStrategy]) -> Sequence[str]:
        """Render every chart and return the paths that were written."""
        self._output_dir.mkdir(parents=True, exist_ok=True)
        written = []
        with plt.rc_context(_BASE_STYLE):
            for chart in charts:
                target = self._output_dir / chart.filename
                LOGGER.info("Rendering %s", target.name)
                written.append(chart.render(frame, str(target)))
        return tuple(written)


def default_charts() -> Sequence[ChartStrategy]:
    """The exploratory figure set required by Activity 2."""
    return (
        PriceDistributionChart(),
        PriceByRoomTypeChart(),
        PriceVsCapacityChart(),
        PriceByCityChart(),
        MissingValuesChart(),
    )
