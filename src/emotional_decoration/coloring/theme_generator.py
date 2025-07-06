"""Theme generation system for emotional-decoration."""

import random
from typing import Dict, List, Optional, Tuple
from ..models import (
    ContentProfile, ColorScheme, VisualEffect, ThemeConfig, 
    EmotionType, ContentType, DifficultyLevel
)
from ..themes.theme_loader import ThemeLoader


class ThemeGenerator:
    """Generates color schemes and visual effects based on content analysis."""
    
    def __init__(self):
        self.base_color_palettes = self._initialize_base_palettes()
        self.effect_templates = self._initialize_effect_templates()
        self.theme_cache: Dict[str, ThemeConfig] = {}
        self.theme_loader = ThemeLoader()
        
    def generate_theme(self, profile: ContentProfile, template_type: str = "typewriter") -> ThemeConfig:
        """
        Generate a complete theme configuration based on content profile.
        
        Args:
            profile: Content analysis profile
            template_type: Target scroll-cast template type
            
        Returns:
            ThemeConfig with colors, effects, and metadata
        """
        cache_key = self._generate_cache_key(profile, template_type)
        
        if cache_key in self.theme_cache:
            return self.theme_cache[cache_key]
        
        # First try to use predefined themes
        predefined_theme = self._get_predefined_theme(profile)
        if predefined_theme:
            # Update compatibility for the specific template
            if template_type not in predefined_theme.compatibility:
                predefined_theme.compatibility.append(template_type)
            
            self.theme_cache[cache_key] = predefined_theme
            return predefined_theme
        
        # Fall back to generated theme
        colors = self._generate_color_scheme(profile)
        effects = self._generate_visual_effects(profile, template_type)
        typography = self._generate_typography(profile)
        
        theme_name = self._generate_theme_name(profile)
        theme_config = ThemeConfig(
            name=theme_name,
            description=self._generate_theme_description(profile),
            colors=colors,
            effects=effects,
            typography=typography,
            compatibility=[template_type]
        )
        
        self.theme_cache[cache_key] = theme_config
        return theme_config
    
    def generate_color_scheme(self, profile: ContentProfile) -> ColorScheme:
        """Generate color scheme based on content profile."""
        return self._generate_color_scheme(profile)
    
    def generate_visual_effects(self, profile: ContentProfile, template_type: str = "typewriter") -> VisualEffect:
        """Generate visual effects based on content profile."""
        return self._generate_visual_effects(profile, template_type)
    
    def _initialize_base_palettes(self) -> Dict[str, Dict[str, str]]:
        """Initialize base color palettes for different themes."""
        return {
            # Learning themes
            "learning_focused": {
                "primary_start": "#4A90E2",
                "primary_end": "#7ED321",
                "background_start": "#000428",
                "background_end": "#004e92",
                "accent_color": "#50E3C2",
                "glow_color": "#4A90E2"
            },
            "learning_energetic": {
                "primary_start": "#FF6B6B",
                "primary_end": "#4ECDC4",
                "background_start": "#134E5E",
                "background_end": "#71B280",
                "accent_color": "#45B7D1",
                "glow_color": "#FF6B6B"
            },
            "learning_supportive": {
                "primary_start": "#A8E6CF",
                "primary_end": "#88D8A3",
                "background_start": "#2C3E50",
                "background_end": "#4A6741",
                "accent_color": "#7FB069",
                "glow_color": "#A8E6CF"
            },
            "learning_accessible": {
                "primary_start": "#6C5CE7",
                "primary_end": "#A29BFE",
                "background_start": "#2D3436",
                "background_end": "#636E72",
                "accent_color": "#74B9FF",
                "glow_color": "#6C5CE7"
            },
            
            # Professional themes
            "professional_minimal": {
                "primary_start": "#2F3542",
                "primary_end": "#57606F",
                "background_start": "#F8F9FA",
                "background_end": "#E9ECEF",
                "accent_color": "#3742FA",
                "glow_color": "#2F3542"
            },
            "professional_positive": {
                "primary_start": "#00B894",
                "primary_end": "#00CEC9",
                "background_start": "#DDD6FE",
                "background_end": "#E0E7FF",
                "accent_color": "#0984E3",
                "glow_color": "#00B894"
            },
            "professional_subtle": {
                "primary_start": "#636E72",
                "primary_end": "#B2BEC3",
                "background_start": "#2D3436",
                "background_end": "#636E72",
                "accent_color": "#74B9FF",
                "glow_color": "#636E72"
            },
            "professional_sophisticated": {
                "primary_start": "#2D3436",
                "primary_end": "#636E72",
                "background_start": "#1A1A1A",
                "background_end": "#2D3436",
                "accent_color": "#FDCB6E",
                "glow_color": "#2D3436"
            },
            
            # Emotional themes
            "emotional_vibrant": {
                "primary_start": "#FF7675",
                "primary_end": "#FDCB6E",
                "background_start": "#6C5CE7",
                "background_end": "#A29BFE",
                "accent_color": "#FD79A8",
                "glow_color": "#FF7675"
            },
            "emotional_serene": {
                "primary_start": "#81ECEC",
                "primary_end": "#74B9FF",
                "background_start": "#2D3436",
                "background_end": "#636E72",
                "accent_color": "#00B894",
                "glow_color": "#81ECEC"
            },
            "emotional_contemplative": {
                "primary_start": "#A29BFE",
                "primary_end": "#6C5CE7",
                "background_start": "#2D3436",
                "background_end": "#636E72",
                "accent_color": "#74B9FF",
                "glow_color": "#A29BFE"
            }
        }
    
    def _initialize_effect_templates(self) -> Dict[str, Dict[str, any]]:
        """Initialize visual effect templates."""
        return {
            "subtle": {
                "glow_intensity": 0.2,
                "animation_speed": 1.0,
                "blur_radius": 0.0,
                "pulse_enabled": False,
                "gradient_angle": 45,
                "shadow_enabled": True,
                "shadow_intensity": 0.3
            },
            "moderate": {
                "glow_intensity": 0.4,
                "animation_speed": 1.0,
                "blur_radius": 0.5,
                "pulse_enabled": True,
                "gradient_angle": 90,
                "shadow_enabled": True,
                "shadow_intensity": 0.5
            },
            "vibrant": {
                "glow_intensity": 0.6,
                "animation_speed": 1.2,
                "blur_radius": 1.0,
                "pulse_enabled": True,
                "gradient_angle": 135,
                "shadow_enabled": True,
                "shadow_intensity": 0.7
            },
            "energetic": {
                "glow_intensity": 0.8,
                "animation_speed": 1.5,
                "blur_radius": 1.5,
                "pulse_enabled": True,
                "gradient_angle": 180,
                "shadow_enabled": True,
                "shadow_intensity": 0.8
            }
        }
    
    def _generate_color_scheme(self, profile: ContentProfile) -> ColorScheme:
        """Generate color scheme based on content profile."""
        theme_key = profile.recommended_theme
        
        # Get base palette
        if theme_key in self.base_color_palettes:
            base_colors = self.base_color_palettes[theme_key]
        else:
            # Generate colors based on emotion and content type
            base_colors = self._generate_colors_from_profile(profile)
        
        # Apply emotion-based modifications
        adjusted_colors = self._adjust_colors_for_emotion(base_colors, profile)
        
        # Apply intensity adjustments
        final_colors = self._adjust_colors_for_intensity(adjusted_colors, profile)
        
        return ColorScheme(**final_colors)
    
    def _get_predefined_theme(self, profile: ContentProfile) -> Optional[ThemeConfig]:
        """Get predefined theme based on content profile."""
        # Find suitable themes using theme loader
        recommended_themes = self.theme_loader.find_themes_for_profile(
            profile.emotion.value,
            profile.content_type.value,
            profile.difficulty.value
        )
        
        if recommended_themes:
            # Use the first (best) recommendation
            theme_name = recommended_themes[0]
            return self.theme_loader.get_theme(theme_name)
        
        return None
    
    def _generate_colors_from_profile(self, profile: ContentProfile) -> Dict[str, str]:
        """Generate colors based on emotion and content type."""
        emotion_colors = {
            EmotionType.HAPPY: {
                "primary_start": "#FFD93D",
                "primary_end": "#FF6B6B",
                "background_start": "#74B9FF",
                "background_end": "#0984E3",
                "accent_color": "#00B894",
                "glow_color": "#FFD93D"
            },
            EmotionType.EXCITED: {
                "primary_start": "#FF6B6B",
                "primary_end": "#4ECDC4",
                "background_start": "#A29BFE",
                "background_end": "#6C5CE7",
                "accent_color": "#FDCB6E",
                "glow_color": "#FF6B6B"
            },
            EmotionType.CALM: {
                "primary_start": "#81ECEC",
                "primary_end": "#74B9FF",
                "background_start": "#2D3436",
                "background_end": "#636E72",
                "accent_color": "#00B894",
                "glow_color": "#81ECEC"
            },
            EmotionType.SAD: {
                "primary_start": "#A29BFE",
                "primary_end": "#6C5CE7",
                "background_start": "#2D3436",
                "background_end": "#636E72",
                "accent_color": "#74B9FF",
                "glow_color": "#A29BFE"
            },
            EmotionType.ANGRY: {
                "primary_start": "#E17055",
                "primary_end": "#D63031",
                "background_start": "#2D3436",
                "background_end": "#636E72",
                "accent_color": "#FDCB6E",
                "glow_color": "#E17055"
            },
            EmotionType.FEARFUL: {
                "primary_start": "#636E72",
                "primary_end": "#B2BEC3",
                "background_start": "#2D3436",
                "background_end": "#636E72",
                "accent_color": "#74B9FF",
                "glow_color": "#636E72"
            },
            EmotionType.SURPRISED: {
                "primary_start": "#FDCB6E",
                "primary_end": "#E17055",
                "background_start": "#6C5CE7",
                "background_end": "#A29BFE",
                "accent_color": "#FF7675",
                "glow_color": "#FDCB6E"
            },
            EmotionType.NEUTRAL: {
                "primary_start": "#2F3542",
                "primary_end": "#57606F",
                "background_start": "#F8F9FA",
                "background_end": "#E9ECEF",
                "accent_color": "#3742FA",
                "glow_color": "#2F3542"
            }
        }
        
        base_colors = emotion_colors.get(profile.emotion, emotion_colors[EmotionType.NEUTRAL])
        
        # Adjust for content type
        if profile.content_type == ContentType.LEARNING:
            base_colors = self._blend_colors(base_colors, self.base_color_palettes["learning_focused"])
        elif profile.content_type == ContentType.PROFESSIONAL:
            base_colors = self._blend_colors(base_colors, self.base_color_palettes["professional_minimal"])
        
        return base_colors
    
    def _adjust_colors_for_emotion(self, colors: Dict[str, str], profile: ContentProfile) -> Dict[str, str]:
        """Adjust colors based on emotion intensity."""
        adjusted = colors.copy()
        
        # Increase saturation for high emotion intensity
        if profile.emotion_intensity > 0.7:
            adjusted = self._increase_saturation(adjusted, 0.2)
        elif profile.emotion_intensity < 0.3:
            adjusted = self._decrease_saturation(adjusted, 0.2)
        
        return adjusted
    
    def _adjust_colors_for_intensity(self, colors: Dict[str, str], profile: ContentProfile) -> Dict[str, str]:
        """Apply final intensity adjustments."""
        adjusted = colors.copy()
        
        # Adjust brightness based on difficulty
        if profile.difficulty == DifficultyLevel.EXPERT:
            adjusted = self._adjust_brightness(adjusted, -0.1)
        elif profile.difficulty == DifficultyLevel.EASY:
            adjusted = self._adjust_brightness(adjusted, 0.1)
        
        return adjusted
    
    def _generate_visual_effects(self, profile: ContentProfile, template_type: str) -> VisualEffect:
        """Generate visual effects based on content profile."""
        # Base effect intensity on emotion
        if profile.emotion_intensity > 0.8:
            base_effect = "energetic"
        elif profile.emotion_intensity > 0.6:
            base_effect = "vibrant"
        elif profile.emotion_intensity > 0.3:
            base_effect = "moderate"
        else:
            base_effect = "subtle"
        
        effect_config = self.effect_templates[base_effect].copy()
        
        # Adjust for content type
        if profile.content_type == ContentType.LEARNING:
            effect_config["animation_speed"] *= 0.8  # Slower for learning
            effect_config["glow_intensity"] *= 0.9
        elif profile.content_type == ContentType.PROFESSIONAL:
            effect_config["animation_speed"] *= 0.7  # Much slower for professional
            effect_config["glow_intensity"] *= 0.6
            effect_config["pulse_enabled"] = False
        elif profile.content_type == ContentType.ENTERTAINMENT:
            effect_config["animation_speed"] *= 1.2  # Faster for entertainment
            effect_config["glow_intensity"] *= 1.1
        
        # Adjust for template type
        if template_type == "railway":
            effect_config["gradient_angle"] = 0  # Horizontal for railway
        elif template_type == "scroll":
            effect_config["animation_speed"] *= 0.8  # Slower for scroll
        
        return VisualEffect(**effect_config)
    
    def _generate_typography(self, profile: ContentProfile) -> Dict[str, any]:
        """Generate typography settings based on content profile."""
        typography = {
            "font_weight": "normal",
            "letter_spacing": "normal",
            "line_height": "1.6",
            "text_transform": "none"
        }
        
        # Adjust for content type
        if profile.content_type == ContentType.PROFESSIONAL:
            typography["font_weight"] = "500"
            typography["letter_spacing"] = "0.01em"
        elif profile.content_type == ContentType.LEARNING:
            typography["line_height"] = "1.8"
            typography["letter_spacing"] = "0.02em"
        elif profile.content_type == ContentType.CREATIVE:
            typography["font_weight"] = "300"
            typography["letter_spacing"] = "0.05em"
        
        # Adjust for difficulty
        if profile.difficulty == DifficultyLevel.EXPERT:
            typography["font_weight"] = "600"
            typography["letter_spacing"] = "0.01em"
        elif profile.difficulty == DifficultyLevel.EASY:
            typography["font_weight"] = "400"
            typography["letter_spacing"] = "0.03em"
        
        return typography
    
    def _generate_theme_name(self, profile: ContentProfile) -> str:
        """Generate a descriptive theme name."""
        emotion_name = profile.emotion.value.title()
        content_name = profile.content_type.value.title()
        intensity = "High" if profile.emotion_intensity > 0.6 else "Low"
        
        return f"{emotion_name} {content_name} ({intensity} Intensity)"
    
    def _generate_theme_description(self, profile: ContentProfile) -> str:
        """Generate a theme description."""
        return (
            f"A {profile.emotion.value} theme optimized for {profile.content_type.value} content "
            f"with {profile.difficulty.value} difficulty level and "
            f"{profile.emotion_intensity:.1f} emotion intensity."
        )
    
    def _generate_cache_key(self, profile: ContentProfile, template_type: str) -> str:
        """Generate a cache key for the theme."""
        return f"{profile.emotion.value}_{profile.content_type.value}_{profile.difficulty.value}_{template_type}_{profile.emotion_intensity:.1f}"
    
    def _blend_colors(self, color1: Dict[str, str], color2: Dict[str, str], ratio: float = 0.5) -> Dict[str, str]:
        """Blend two color dictionaries."""
        blended = {}
        for key in color1:
            if key in color2:
                blended[key] = self._blend_hex_colors(color1[key], color2[key], ratio)
            else:
                blended[key] = color1[key]
        return blended
    
    def _blend_hex_colors(self, color1: str, color2: str, ratio: float = 0.5) -> str:
        """Blend two hex colors."""
        # Convert hex to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Convert RGB to hex
        def rgb_to_hex(rgb):
            return '#%02x%02x%02x' % rgb
        
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        
        # Blend
        blended_rgb = tuple(int(rgb1[i] * (1 - ratio) + rgb2[i] * ratio) for i in range(3))
        
        return rgb_to_hex(blended_rgb)
    
    def _increase_saturation(self, colors: Dict[str, str], amount: float) -> Dict[str, str]:
        """Increase color saturation."""
        # Simplified saturation increase
        return colors  # Implementation would involve HSL conversion
    
    def _decrease_saturation(self, colors: Dict[str, str], amount: float) -> Dict[str, str]:
        """Decrease color saturation."""
        # Simplified saturation decrease
        return colors  # Implementation would involve HSL conversion
    
    def _adjust_brightness(self, colors: Dict[str, str], amount: float) -> Dict[str, str]:
        """Adjust color brightness."""
        # Simplified brightness adjustment
        return colors  # Implementation would involve HSL conversion