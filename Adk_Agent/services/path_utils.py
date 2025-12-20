from pathlib import Path


def get_data_dir() -> Path:
    """Return the data directory for this app.
    Prefers package-relative `data` folder; falls back to workspace root `data`.
    """
    # Package root: Adk_Agent
    pkg_root = Path(__file__).resolve().parents[1]
    pkg_data = pkg_root / "data"
    if pkg_data.exists():
        return pkg_data

    # Workspace root
    ws_root = pkg_root.parent
    ws_data = ws_root / "data"
    if ws_data.exists():
        return ws_data

    # Ensure package data directory for future writes
    pkg_data.mkdir(parents=True, exist_ok=True)
    return pkg_data
