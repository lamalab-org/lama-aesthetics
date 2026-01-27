import importlib.resources

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.font_manager import FontProperties
from scipy.constants import golden

# Track whether fonts have been registered
_fonts_registered = False


def register_fonts() -> None:
    """Register bundled fonts with Matplotlib's font manager.

    This function adds the CMU Sans Serif font bundled with the package
    to Matplotlib's font manager, allowing it to be used without system-wide
    installation. Safe to call multiple times (will only register once).
    """
    global _fonts_registered
    if _fonts_registered:
        return

    # Get path to the bundled font
    font_files = ["cmunss.otf"]

    for font_file in font_files:
        with importlib.resources.as_file(importlib.resources.files("lama_aesthetics.fonts").joinpath(font_file)) as font_path:
            font_manager.fontManager.addfont(str(font_path))

    _fonts_registered = True


def get_font_name() -> str:
    """Get the family name of the bundled CMU Sans Serif font.

    Returns:
        The font family name as recognized by Matplotlib.
    """
    with importlib.resources.as_file(importlib.resources.files("lama_aesthetics.fonts").joinpath("cmunss.otf")) as font_path:
        return FontProperties(fname=str(font_path)).get_name()


STYLES = {
    "main": "lamalab.mplstyle",
    "presentation": "presentation.mplstyle",
    "dark": "lamalab_dark.mplstyle",
}

# Figure dimensions
ONE_COL_WIDTH = 3
TWO_COL_WIDTH = 7.25
ONE_COL_HEIGHT = ONE_COL_WIDTH / golden
TWO_COL_HEIGHT = TWO_COL_WIDTH / golden


def get_style(style_name: str) -> None:
    """Get the path to a matplotlib style file and apply it.

    This function registers bundled fonts before applying the style,
    ensuring the CMU Sans Serif font is available without system installation.

    Args:
        style_name: Name of the style ('main', 'presentation', or 'dark')

    Raises:
        KeyError: If style_name is not in STYLES dictionary
    """
    if style_name not in STYLES:
        raise KeyError(f"Style '{style_name}' not found. Available styles: {list(STYLES.keys())}")

    # Register bundled fonts before applying the style
    register_fonts()

    style_file = STYLES[style_name]

    # Get the file contents as a string
    # This will only work for Python 3.7 and later
    with importlib.resources.path("lama_aesthetics.styles", style_file) as style_path:
        plt.style.use(style_path)

    return
