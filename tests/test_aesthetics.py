import pytest

from lama_aesthetics.aesthetics import (
    ONE_COL_HEIGHT,
    ONE_COL_WIDTH,
    STYLES,
    TWO_COL_HEIGHT,
    TWO_COL_WIDTH,
    get_style,
)


def test_styles_dict():
    """Test that STYLES dictionary is properly defined."""
    assert isinstance(STYLES, dict)
    assert "main" in STYLES
    assert "presentation" in STYLES


def test_constants():
    """Test that dimension constants are defined and have reasonable values."""
    assert ONE_COL_WIDTH == 3
    assert TWO_COL_WIDTH == 7.25
    assert ONE_COL_HEIGHT > 0
    assert TWO_COL_HEIGHT > 0
    assert TWO_COL_WIDTH > ONE_COL_WIDTH
    assert TWO_COL_HEIGHT > ONE_COL_HEIGHT


def test_get_style_valid():
    """Test that get_style works with valid style names."""
    # Should not raise an exception
    get_style("main")
    get_style("presentation")


def test_get_style_invalid():
    """Test that get_style raises KeyError for invalid style names."""
    with pytest.raises(KeyError, match="Style 'invalid' not found"):
        get_style("invalid")
