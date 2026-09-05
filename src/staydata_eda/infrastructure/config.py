"""Runtime configuration.

Paths are resolved from environment variables so the very same code runs on a
laptop and inside the Docker image without edits.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _project_root() -> Path:
    """Return the repository root (three levels above this file)."""
    return Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Settings:
    """Immutable application settings."""

    raw_data_path: Path
    cache_path: Path
    figures_dir: Path
    sheet_name: str = "in"

    @classmethod
    def from_env(cls) -> "Settings":
        """Build settings from environment variables with sensible defaults."""
        root = Path(os.getenv("PROJECT_ROOT", str(_project_root())))
        return cls(
            raw_data_path=Path(
                os.getenv("RAW_DATA_PATH", str(root / "data" / "raw" / "airbnb_price_prediction.xlsx"))
            ),
            cache_path=Path(
                os.getenv("CACHE_PATH", str(root / "data" / "interim" / "listings.parquet"))
            ),
            figures_dir=Path(os.getenv("FIGURES_DIR", str(root / "reports" / "figures"))),
            sheet_name=os.getenv("SHEET_NAME", "in"),
        )

    def ensure_directories(self) -> None:
        """Create the output directories when they do not exist yet."""
        self.figures_dir.mkdir(parents=True, exist_ok=True)
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
