"""Theme configuration loader for emotional-decoration system."""

import yaml
from pathlib import Path
from typing import Dict, List, Optional
from ..models import ThemeConfig, ColorScheme, VisualEffect


class ThemeLoader:
    """Loads and manages theme configurations from YAML files."""
    
    def __init__(self, themes_dir: Optional[str] = None):
        if themes_dir:
            self.themes_dir = Path(themes_dir)
        else:
            # Default to themes directory in project root
            self.themes_dir = Path(__file__).parent.parent.parent.parent / "themes"
        
        self.loaded_themes: Dict[str, ThemeConfig] = {}
        self._load_all_themes()
    
    def _load_all_themes(self):
        """Load all theme YAML files from the themes directory."""
        if not self.themes_dir.exists():
            return
        
        # Recursively find all YAML files in themes directory
        for yaml_file in self.themes_dir.rglob("*.yaml"):
            try:
                theme_config = self._load_theme_file(yaml_file)
                if theme_config:
                    # Use filename (without extension) as theme key
                    theme_key = yaml_file.stem
                    self.loaded_themes[theme_key] = theme_config
            except Exception as e:
                print(f"Warning: Failed to load theme from {yaml_file}: {e}")
    
    def _load_theme_file(self, yaml_file: Path) -> Optional[ThemeConfig]:
        """Load a single theme YAML file."""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            theme_data = yaml.safe_load(f)
        
        if not theme_data:
            return None
        
        # Extract and validate required fields
        name = theme_data.get('name')
        description = theme_data.get('description', '')
        
        if not name:
            raise ValueError(f"Theme file {yaml_file} missing required 'name' field")
        
        # Parse colors
        colors_data = theme_data.get('colors', {})
        colors = ColorScheme(
            primary_start=colors_data.get('primary_start', '#4A90E2'),
            primary_end=colors_data.get('primary_end', '#7ED321'),
            background_start=colors_data.get('background_start', '#000428'),
            background_end=colors_data.get('background_end', '#004e92'),
            accent_color=colors_data.get('accent_color', '#50E3C2'),
            glow_color=colors_data.get('glow_color', '#4A90E2')
        )
        
        # Parse effects
        effects_data = theme_data.get('effects', {})
        effects = VisualEffect(
            glow_intensity=effects_data.get('glow_intensity', 0.3),
            animation_speed=effects_data.get('animation_speed', 1.0),
            blur_radius=effects_data.get('blur_radius', 0.0),
            pulse_enabled=effects_data.get('pulse_enabled', False),
            gradient_angle=effects_data.get('gradient_angle', 45),
            shadow_enabled=effects_data.get('shadow_enabled', True),
            shadow_intensity=effects_data.get('shadow_intensity', 0.5)
        )
        
        # Parse typography
        typography = theme_data.get('typography', {})
        
        # Parse compatibility
        compatibility = theme_data.get('compatibility', ['typewriter'])
        
        return ThemeConfig(
            name=name,
            description=description,
            colors=colors,
            effects=effects,
            typography=typography,
            compatibility=compatibility
        )
    
    def get_theme(self, theme_name: str) -> Optional[ThemeConfig]:
        """
        Get a theme by name.
        
        Args:
            theme_name: Name of the theme to retrieve
            
        Returns:
            ThemeConfig if found, None otherwise
        """
        return self.loaded_themes.get(theme_name)
    
    def list_themes(self) -> List[str]:
        """
        List all available theme names.
        
        Returns:
            List of theme names
        """
        return list(self.loaded_themes.keys())
    
    def list_themes_by_category(self, category: str) -> List[str]:
        """
        List themes filtered by category.
        
        Args:
            category: Category to filter by (learning, emotional, professional)
            
        Returns:
            List of theme names in the category
        """
        category_themes = []
        for theme_name, theme_config in self.loaded_themes.items():
            # Check if theme name starts with category
            if theme_name.startswith(category):
                category_themes.append(theme_name)
        
        return category_themes
    
    def get_theme_info(self, theme_name: str) -> Optional[Dict[str, any]]:
        """
        Get detailed information about a theme.
        
        Args:
            theme_name: Name of the theme
            
        Returns:
            Dictionary with theme information
        """
        theme = self.get_theme(theme_name)
        if not theme:
            return None
        
        return {
            'name': theme.name,
            'description': theme.description,
            'category': self._extract_category(theme_name),
            'colors': {
                'primary_gradient': [theme.colors.primary_start, theme.colors.primary_end],
                'background_gradient': [theme.colors.background_start, theme.colors.background_end],
                'accent': theme.colors.accent_color,
                'glow': theme.colors.glow_color
            },
            'effects': {
                'glow_intensity': theme.effects.glow_intensity,
                'animation_speed': theme.effects.animation_speed,
                'pulse_enabled': theme.effects.pulse_enabled,
                'gradient_angle': theme.effects.gradient_angle
            },
            'compatibility': theme.compatibility,
            'typography': theme.typography
        }
    
    def find_themes_for_profile(self, emotion: str, content_type: str, difficulty: str) -> List[str]:
        """
        Find suitable themes based on content profile.
        
        Args:
            emotion: Detected emotion
            content_type: Content type
            difficulty: Difficulty level
            
        Returns:
            List of recommended theme names
        """
        recommendations = []
        
        # Primary recommendation based on content type
        if content_type == 'learning':
            if difficulty in ['easy', 'medium']:
                recommendations.append('learning_energetic')
            else:
                recommendations.append('learning_focused')
        elif content_type == 'professional':
            if emotion in ['happy', 'excited']:
                recommendations.append('professional_positive')
            else:
                recommendations.append('professional_minimal')
        elif content_type in ['narrative', 'creative', 'entertainment']:
            if emotion in ['happy', 'excited']:
                recommendations.append('emotional_vibrant')
            elif emotion in ['calm', 'neutral']:
                recommendations.append('emotional_serene')
            else:
                recommendations.append('emotional_vibrant')  # Default for emotional content
        
        # Add fallbacks
        if content_type == 'learning':
            recommendations.extend(['learning_focused', 'learning_energetic'])
        elif content_type == 'professional':
            recommendations.extend(['professional_minimal', 'professional_positive'])
        else:
            recommendations.extend(['emotional_serene', 'emotional_vibrant'])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recommendations = []
        for theme in recommendations:
            if theme not in seen and theme in self.loaded_themes:
                seen.add(theme)
                unique_recommendations.append(theme)
        
        return unique_recommendations[:3]  # Return top 3 recommendations
    
    def _extract_category(self, theme_name: str) -> str:
        """Extract category from theme name."""
        if theme_name.startswith('learning'):
            return 'learning'
        elif theme_name.startswith('professional'):
            return 'professional'
        elif theme_name.startswith('emotional'):
            return 'emotional'
        else:
            return 'custom'
    
    def reload_themes(self):
        """Reload all themes from disk."""
        self.loaded_themes.clear()
        self._load_all_themes()
    
    def add_custom_theme(self, theme_name: str, theme_config: ThemeConfig):
        """
        Add a custom theme configuration.
        
        Args:
            theme_name: Name for the custom theme
            theme_config: Theme configuration
        """
        self.loaded_themes[theme_name] = theme_config
    
    def save_custom_theme(self, theme_name: str, theme_config: ThemeConfig, 
                         custom_themes_dir: Optional[str] = None):
        """
        Save a custom theme to a YAML file.
        
        Args:
            theme_name: Name for the theme file
            theme_config: Theme configuration to save
            custom_themes_dir: Optional directory for custom themes
        """
        if custom_themes_dir:
            save_dir = Path(custom_themes_dir)
        else:
            save_dir = self.themes_dir / "custom"
        
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Convert theme config to YAML-serializable format
        theme_data = {
            'name': theme_config.name,
            'description': theme_config.description,
            'colors': {
                'primary_start': theme_config.colors.primary_start,
                'primary_end': theme_config.colors.primary_end,
                'background_start': theme_config.colors.background_start,
                'background_end': theme_config.colors.background_end,
                'accent_color': theme_config.colors.accent_color,
                'glow_color': theme_config.colors.glow_color
            },
            'effects': {
                'glow_intensity': theme_config.effects.glow_intensity,
                'animation_speed': theme_config.effects.animation_speed,
                'blur_radius': theme_config.effects.blur_radius,
                'pulse_enabled': theme_config.effects.pulse_enabled,
                'gradient_angle': theme_config.effects.gradient_angle,
                'shadow_enabled': theme_config.effects.shadow_enabled,
                'shadow_intensity': theme_config.effects.shadow_intensity
            },
            'typography': theme_config.typography,
            'compatibility': theme_config.compatibility
        }
        
        # Save to YAML file
        yaml_file = save_dir / f"{theme_name}.yaml"
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(theme_data, f, default_flow_style=False, indent=2)
        
        # Add to loaded themes
        self.loaded_themes[theme_name] = theme_config