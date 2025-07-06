"""
emotional-decoration: Visual enhancement system for scroll-cast content.

This package provides intelligent content analysis and decoration generation
to enhance the visual appeal of scroll-cast animations through CSS override
architecture.
"""

__version__ = "1.0.0"
__author__ = "emotional-decoration Team"
__email__ = "contact@emotional-decoration.dev"

from .boxing.content_analyzer import ContentAnalyzer
from .coloring.theme_generator import ThemeGenerator
from .packing.css_generator import CSSGenerator
from .rendering.decoration_renderer import DecorationRenderer
from .rendering.html_injector import HTMLInjector
from .orchestrator.decoration_engine import DecorationEngine
from .themes.theme_loader import ThemeLoader

__all__ = [
    "ContentAnalyzer",
    "ThemeGenerator", 
    "CSSGenerator",
    "DecorationRenderer",
    "HTMLInjector",
    "DecorationEngine",
    "ThemeLoader",
]