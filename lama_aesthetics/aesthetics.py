import importlib.resources

import matplotlib.pyplot as plt

STYLES = {
    "main": "lamalab.mplstyle",
    "presentation": "presentation.mplstyle",
}


def get_style(style_name: str) -> None:
    """Get the path to a matplotlib style file and apply it.

    Args:
        style_name: Name of the style ('main' or 'presentation')

    Raises:
        KeyError: If style_name is not in STYLES dictionary
    """
    if style_name not in STYLES:
        raise KeyError(f"Style '{style_name}' not found. Available styles: {list(STYLES.keys())}")

    style_file = STYLES[style_name]

    # Get the file contents as a string
    # This will only work for Python 3.7 and later
    with importlib.resources.path("lama_aesthetics.styles", style_file) as style_path:
        plt.style.use(style_path)

    return
