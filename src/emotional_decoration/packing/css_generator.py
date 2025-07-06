"""CSS generation system for emotional-decoration."""

from typing import Dict, List, Optional, Tuple
from ..models import ThemeConfig, ColorScheme, VisualEffect


class CSSGenerator:
    """Generates CSS styles for emotional decoration that integrates with scroll-cast."""
    
    def __init__(self):
        self.css_templates = self._initialize_css_templates()
        self.compatibility_rules = self._initialize_compatibility_rules()
        
    def generate_css(self, theme_config: ThemeConfig, template_type: str = "typewriter") -> str:
        """
        Generate CSS for the given theme configuration.
        
        Args:
            theme_config: Theme configuration containing colors and effects
            template_type: Target scroll-cast template type
            
        Returns:
            Generated CSS string
        """
        css_parts = []
        
        # Add CSS header with metadata
        css_parts.append(self._generate_css_header(theme_config))
        
        # Add CSS custom properties (variables)
        css_parts.append(self._generate_css_variables(theme_config))
        
        # Add base decoration styles
        css_parts.append(self._generate_base_decoration_styles(theme_config))
        
        # Add template-specific styles
        css_parts.append(self._generate_template_styles(theme_config, template_type))
        
        # Add animation styles
        css_parts.append(self._generate_animation_styles(theme_config))
        
        # Add responsive styles
        css_parts.append(self._generate_responsive_styles(theme_config))
        
        # Add accessibility styles
        css_parts.append(self._generate_accessibility_styles(theme_config))
        
        return "\n\n".join(css_parts)
    
    def generate_minified_css(self, theme_config: ThemeConfig, template_type: str = "typewriter") -> str:
        """Generate minified CSS for production use."""
        css = self.generate_css(theme_config, template_type)
        return self._minify_css(css)
    
    def _initialize_css_templates(self) -> Dict[str, str]:
        """Initialize CSS templates for different components."""
        return {
            "typewriter": """
/* Typewriter Template Decoration */
.typewriter-char {
    /* Core functionality preserved from scroll-cast */
    /* opacity, transition, display are controlled by scroll-cast */
    
    /* Decoration enhancements */
    background: linear-gradient(var(--decoration-gradient-angle), var(--decoration-primary-start), var(--decoration-primary-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    
    /* Glow effect */
    filter: drop-shadow(0 0 var(--decoration-glow-radius) var(--decoration-glow-color));
    
    /* Animation enhancement */
    animation: decorationEnhance var(--decoration-animation-duration) ease-in-out;
}

.typewriter-char.decoration-enhanced {
    /* Additional styling when decoration is active */
    position: relative;
    z-index: 1;
}

.typewriter-char::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: var(--decoration-accent-color);
    opacity: var(--decoration-glow-intensity);
    border-radius: 2px;
    z-index: -1;
    filter: blur(var(--decoration-blur-radius));
}

.typewriter-container {
    /* Container decoration */
    background: linear-gradient(var(--decoration-bg-angle), var(--decoration-bg-start), var(--decoration-bg-end));
    padding: var(--decoration-container-padding);
    border-radius: var(--decoration-border-radius);
}

.typewriter-sentence {
    /* Sentence-level decoration */
    position: relative;
    margin: var(--decoration-sentence-margin);
}
""",
            "railway": """
/* Railway Template Decoration */
.railway-line {
    /* Core functionality preserved from scroll-cast */
    
    /* Decoration enhancements */
    background: linear-gradient(to right, var(--decoration-primary-start), var(--decoration-primary-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    
    /* Railway-specific glow */
    box-shadow: 0 0 var(--decoration-glow-radius) var(--decoration-glow-color);
    
    /* Motion enhancement */
    animation: railwayGlow var(--decoration-animation-duration) ease-in-out infinite;
}

.railway-container {
    /* Container decoration with railway theme */
    background: linear-gradient(180deg, var(--decoration-bg-start), var(--decoration-bg-end));
    border-top: 2px solid var(--decoration-accent-color);
    border-bottom: 2px solid var(--decoration-accent-color);
    position: relative;
}

.railway-container::before,
.railway-container::after {
    content: '';
    position: absolute;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(to right, transparent, var(--decoration-accent-color), transparent);
}

.railway-container::before {
    top: 10px;
}

.railway-container::after {
    bottom: 10px;
}
""",
            "scroll": """
/* Scroll Template Decoration */
.scroll-line {
    /* Core functionality preserved from scroll-cast */
    
    /* Decoration enhancements */
    background: linear-gradient(var(--decoration-gradient-angle), var(--decoration-primary-start), var(--decoration-primary-end));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    
    /* Scroll-specific effects */
    filter: drop-shadow(0 2px var(--decoration-glow-radius) var(--decoration-glow-color));
    
    /* Smooth scrolling enhancement */
    animation: scrollDecoration var(--decoration-animation-duration) ease-out;
}

.scroll-container {
    /* Container decoration with scroll theme */
    background: linear-gradient(var(--decoration-bg-angle), var(--decoration-bg-start), var(--decoration-bg-end));
    mask: linear-gradient(to bottom, transparent, black 20%, black 80%, transparent);
    -webkit-mask: linear-gradient(to bottom, transparent, black 20%, black 80%, transparent);
}

.scroll-line.decoration-enhanced {
    /* Enhanced scroll line */
    position: relative;
    overflow: hidden;
}

.scroll-line.decoration-enhanced::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, var(--decoration-accent-color), transparent);
    animation: scrollShimmer var(--decoration-animation-duration) ease-in-out;
}
"""
        }
    
    def _initialize_compatibility_rules(self) -> Dict[str, Dict[str, str]]:
        """Initialize compatibility rules for different scroll-cast templates."""
        return {
            "typewriter": {
                "preserve_opacity": "opacity",
                "preserve_transition": "transition",
                "preserve_display": "display",
                "preserve_position": "position"
            },
            "railway": {
                "preserve_transform": "transform",
                "preserve_transition": "transition",
                "preserve_position": "position"
            },
            "scroll": {
                "preserve_transform": "transform",
                "preserve_transition": "transition",
                "preserve_overflow": "overflow"
            }
        }
    
    def _generate_css_header(self, theme_config: ThemeConfig) -> str:
        """Generate CSS header with metadata."""
        return f"""/*
 * Emotional Decoration Theme: {theme_config.name}
 * Description: {theme_config.description}
 * Compatible with: {', '.join(theme_config.compatibility)}
 * 
 * This CSS enhances scroll-cast animations without breaking core functionality.
 * Generated by emotional-decoration system.
 */"""
    
    def _generate_css_variables(self, theme_config: ThemeConfig) -> str:
        """Generate CSS custom properties for theme customization."""
        colors = theme_config.colors
        effects = theme_config.effects
        
        return f""":root {{
    /* Color Variables */
    --decoration-primary-start: {colors.primary_start};
    --decoration-primary-end: {colors.primary_end};
    --decoration-bg-start: {colors.background_start};
    --decoration-bg-end: {colors.background_end};
    --decoration-accent-color: {colors.accent_color};
    --decoration-glow-color: {colors.glow_color};
    
    /* Effect Variables */
    --decoration-glow-intensity: {effects.glow_intensity};
    --decoration-glow-radius: {effects.glow_intensity * 8}px;
    --decoration-animation-duration: {1 / effects.animation_speed}s;
    --decoration-blur-radius: {effects.blur_radius}px;
    --decoration-gradient-angle: {effects.gradient_angle}deg;
    --decoration-bg-angle: {effects.gradient_angle + 45}deg;
    --decoration-shadow-intensity: {effects.shadow_intensity};
    
    /* Layout Variables */
    --decoration-container-padding: {max(10, effects.glow_intensity * 20)}px;
    --decoration-border-radius: {effects.blur_radius * 2}px;
    --decoration-sentence-margin: {effects.glow_intensity * 5}px 0;
    
    /* Typography Variables */
    --decoration-font-weight: {theme_config.typography.get('font_weight', 'normal')};
    --decoration-letter-spacing: {theme_config.typography.get('letter_spacing', 'normal')};
    --decoration-line-height: {theme_config.typography.get('line_height', '1.6')};
    --decoration-text-transform: {theme_config.typography.get('text_transform', 'none')};
}}"""
    
    def _generate_base_decoration_styles(self, theme_config: ThemeConfig) -> str:
        """Generate base decoration styles."""
        return """
/* Base Decoration Styles */
.decoration-enhanced {
    /* Common decoration enhancements */
    font-weight: var(--decoration-font-weight);
    letter-spacing: var(--decoration-letter-spacing);
    line-height: var(--decoration-line-height);
    text-transform: var(--decoration-text-transform);
    
    /* Smooth transitions */
    transition: all 0.3s ease-in-out;
    
    /* Hardware acceleration */
    transform: translateZ(0);
    will-change: transform, opacity, filter;
}

.decoration-enhanced:hover {
    /* Hover effects */
    filter: brightness(1.1) contrast(1.05);
    transform: translateZ(0) scale(1.02);
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    .decoration-enhanced {
        animation: none !important;
        transition: none !important;
    }
    
    .decoration-enhanced:hover {
        transform: none !important;
    }
}"""
    
    def _generate_template_styles(self, theme_config: ThemeConfig, template_type: str) -> str:
        """Generate template-specific styles."""
        template_css = self.css_templates.get(template_type, self.css_templates["typewriter"])
        
        # Add pulse animation if enabled
        if theme_config.effects.pulse_enabled:
            pulse_animation = self._generate_pulse_animation(theme_config)
            template_css += "\n\n" + pulse_animation
        
        return template_css
    
    def _generate_animation_styles(self, theme_config: ThemeConfig) -> str:
        """Generate animation keyframes."""
        animations = []
        
        # Base decoration animation
        animations.append(f"""
@keyframes decorationEnhance {{
    0% {{
        filter: drop-shadow(0 0 0 transparent);
        transform: scale(1);
    }}
    50% {{
        filter: drop-shadow(0 0 var(--decoration-glow-radius) var(--decoration-glow-color));
        transform: scale(1.01);
    }}
    100% {{
        filter: drop-shadow(0 0 var(--decoration-glow-radius) var(--decoration-glow-color));
        transform: scale(1);
    }}
}}""")
        
        # Railway-specific animation
        animations.append(f"""
@keyframes railwayGlow {{
    0%, 100% {{
        box-shadow: 0 0 var(--decoration-glow-radius) var(--decoration-glow-color);
    }}
    50% {{
        box-shadow: 0 0 calc(var(--decoration-glow-radius) * 1.5) var(--decoration-glow-color);
    }}
}}""")
        
        # Scroll-specific animation
        animations.append(f"""
@keyframes scrollDecoration {{
    0% {{
        filter: drop-shadow(0 2px 0 transparent);
        opacity: 0;
    }}
    100% {{
        filter: drop-shadow(0 2px var(--decoration-glow-radius) var(--decoration-glow-color));
        opacity: 1;
    }}
}}""")
        
        # Shimmer effect for scroll
        animations.append(f"""
@keyframes scrollShimmer {{
    0% {{
        left: -100%;
        opacity: 0;
    }}
    50% {{
        opacity: var(--decoration-glow-intensity);
    }}
    100% {{
        left: 100%;
        opacity: 0;
    }}
}}""")
        
        return "\n\n".join(animations)
    
    def _generate_pulse_animation(self, theme_config: ThemeConfig) -> str:
        """Generate pulse animation styles."""
        return f"""
/* Pulse Animation */
@keyframes decorationPulse {{
    0%, 100% {{
        filter: drop-shadow(0 0 var(--decoration-glow-radius) var(--decoration-glow-color));
    }}
    50% {{
        filter: drop-shadow(0 0 calc(var(--decoration-glow-radius) * 1.5) var(--decoration-glow-color)) brightness(1.1);
    }}
}}

.decoration-enhanced.pulse-enabled {{
    animation: decorationPulse calc(var(--decoration-animation-duration) * 2) ease-in-out infinite;
}}"""
    
    def _generate_responsive_styles(self, theme_config: ThemeConfig) -> str:
        """Generate responsive styles for different screen sizes."""
        return """
/* Responsive Styles */
@media (max-width: 768px) {
    :root {
        --decoration-glow-radius: calc(var(--decoration-glow-radius) * 0.8);
        --decoration-container-padding: calc(var(--decoration-container-padding) * 0.8);
    }
    
    .decoration-enhanced {
        /* Reduced effects on mobile */
        filter: none !important;
        transform: none !important;
    }
}

@media (max-width: 480px) {
    :root {
        --decoration-glow-radius: calc(var(--decoration-glow-radius) * 0.6);
        --decoration-container-padding: calc(var(--decoration-container-padding) * 0.6);
    }
}

@media (min-width: 1200px) {
    :root {
        --decoration-glow-radius: calc(var(--decoration-glow-radius) * 1.2);
        --decoration-container-padding: calc(var(--decoration-container-padding) * 1.2);
    }
}"""
    
    def _generate_accessibility_styles(self, theme_config: ThemeConfig) -> str:
        """Generate accessibility-friendly styles."""
        return """
/* Accessibility Styles */
@media (prefers-contrast: high) {
    :root {
        --decoration-glow-intensity: 0.8;
        --decoration-shadow-intensity: 0.9;
    }
    
    .decoration-enhanced {
        /* Higher contrast for accessibility */
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
    }
}

@media (prefers-contrast: low) {
    :root {
        --decoration-glow-intensity: 0.3;
        --decoration-shadow-intensity: 0.3;
    }
}

/* Focus styles for keyboard navigation */
.decoration-enhanced:focus {
    outline: 2px solid var(--decoration-accent-color);
    outline-offset: 2px;
    border-radius: var(--decoration-border-radius);
}

/* High contrast mode support */
@media (prefers-color-scheme: dark) {
    :root {
        --decoration-bg-start: #1a1a1a;
        --decoration-bg-end: #2d2d2d;
    }
}"""
    
    def _minify_css(self, css: str) -> str:
        """Minify CSS by removing unnecessary whitespace and comments."""
        import re
        
        # Remove comments
        css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
        
        # Remove extra whitespace
        css = re.sub(r'\s+', ' ', css)
        
        # Remove whitespace around specific characters
        css = re.sub(r'\s*([{}:;,])\s*', r'\1', css)
        
        # Remove trailing semicolons before closing braces
        css = re.sub(r';\s*}', '}', css)
        
        return css.strip()
    
    def generate_css_manifest(self, theme_config: ThemeConfig) -> Dict[str, any]:
        """Generate CSS manifest with metadata."""
        return {
            "theme_name": theme_config.name,
            "theme_description": theme_config.description,
            "compatibility": theme_config.compatibility,
            "colors": theme_config.colors.dict(),
            "effects": theme_config.effects.dict(),
            "typography": theme_config.typography,
            "css_variables": self._extract_css_variables(theme_config),
            "selectors": self._extract_css_selectors(theme_config)
        }
    
    def _extract_css_variables(self, theme_config: ThemeConfig) -> List[str]:
        """Extract CSS variable names from theme config."""
        return [
            "--decoration-primary-start",
            "--decoration-primary-end",
            "--decoration-bg-start",
            "--decoration-bg-end",
            "--decoration-accent-color",
            "--decoration-glow-color",
            "--decoration-glow-intensity",
            "--decoration-glow-radius",
            "--decoration-animation-duration",
            "--decoration-blur-radius",
            "--decoration-gradient-angle",
            "--decoration-bg-angle",
            "--decoration-shadow-intensity"
        ]
    
    def _extract_css_selectors(self, theme_config: ThemeConfig) -> List[str]:
        """Extract CSS selectors that will be used."""
        base_selectors = [
            ".decoration-enhanced",
            ".decoration-enhanced:hover",
            ".decoration-enhanced:focus"
        ]
        
        # Add template-specific selectors
        for template in theme_config.compatibility:
            if template == "typewriter":
                base_selectors.extend([
                    ".typewriter-char",
                    ".typewriter-container",
                    ".typewriter-sentence"
                ])
            elif template == "railway":
                base_selectors.extend([
                    ".railway-line",
                    ".railway-container"
                ])
            elif template == "scroll":
                base_selectors.extend([
                    ".scroll-line",
                    ".scroll-container"
                ])
        
        return base_selectors