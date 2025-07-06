"""Basic unit tests for emotional-decoration components."""

import pytest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from emotional_decoration.boxing.content_analyzer import ContentAnalyzer
from emotional_decoration.coloring.theme_generator import ThemeGenerator
from emotional_decoration.packing.css_generator import CSSGenerator
from emotional_decoration.models import ContentProfile, EmotionType, ContentType, DifficultyLevel


class TestContentAnalyzer:
    """Test content analysis functionality."""
    
    @pytest.fixture
    def analyzer(self):
        return ContentAnalyzer()
    
    def test_emotion_detection(self, analyzer):
        """Test emotion detection from text."""
        # Happy content
        happy_text = "I'm so excited and happy about this amazing opportunity!"
        result = analyzer.analyze(happy_text)
        assert result.profile.emotion in [EmotionType.HAPPY, EmotionType.EXCITED]
        assert result.profile.emotion_intensity > 0.3
        
        # Calm content
        calm_text = "This is a peaceful and tranquil environment for meditation."
        result = analyzer.analyze(calm_text)
        assert result.profile.emotion in [EmotionType.CALM, EmotionType.NEUTRAL]
        
        # Professional content
        professional_text = "Our quarterly business results show strong growth in revenue and market share."
        result = analyzer.analyze(professional_text)
        assert result.profile.content_type == ContentType.PROFESSIONAL
    
    def test_content_classification(self, analyzer):
        """Test content type classification."""
        # Learning content
        learning_text = "Let's learn about the fundamentals of machine learning and understand the key concepts."
        result = analyzer.analyze(learning_text)
        assert result.profile.content_type == ContentType.LEARNING
        
        # Technical content
        technical_text = "The API endpoint returns JSON data with authentication headers and error handling."
        result = analyzer.analyze(technical_text)
        assert result.profile.content_type in [ContentType.TECHNICAL, ContentType.PROFESSIONAL]
        
        # Creative content
        creative_text = "The artist painted beautiful colors and imaginative forms on the canvas."
        result = analyzer.analyze(creative_text)
        assert result.profile.content_type in [ContentType.CREATIVE, ContentType.NARRATIVE]
    
    def test_difficulty_assessment(self, analyzer):
        """Test reading difficulty assessment."""
        # Simple text
        simple_text = "This is easy to read. Short words. Simple ideas."
        result = analyzer.analyze(simple_text)
        assert result.profile.difficulty in [DifficultyLevel.EASY, DifficultyLevel.MEDIUM]
        
        # Complex text
        complex_text = "The comprehensive implementation of sophisticated algorithmic methodologies necessitates extensive computational resources."
        result = analyzer.analyze(complex_text)
        assert result.profile.difficulty in [DifficultyLevel.HARD, DifficultyLevel.EXPERT]
    
    def test_performance_tracking(self, analyzer):
        """Test performance tracking."""
        text = "Sample text for performance testing."
        result = analyzer.analyze(text)
        
        assert result.processing_time > 0
        assert result.word_count > 0
        assert result.character_count == len(text)
        assert len(result.sentences) > 0


class TestThemeGenerator:
    """Test theme generation functionality."""
    
    @pytest.fixture
    def generator(self):
        return ThemeGenerator()
    
    @pytest.fixture
    def sample_profile(self):
        return ContentProfile(
            emotion=EmotionType.HAPPY,
            content_type=ContentType.LEARNING,
            difficulty=DifficultyLevel.MEDIUM,
            emotion_intensity=0.7,
            reading_speed=250.0,
            recommended_theme="learning_energetic",
            confidence=0.8
        )
    
    def test_theme_generation(self, generator, sample_profile):
        """Test basic theme generation."""
        theme = generator.generate_theme(sample_profile, "typewriter")
        
        assert theme.name is not None
        assert theme.description is not None
        assert theme.colors is not None
        assert theme.effects is not None
        assert "typewriter" in theme.compatibility
    
    def test_color_scheme_generation(self, generator, sample_profile):
        """Test color scheme generation."""
        colors = generator.generate_color_scheme(sample_profile)
        
        # Check that all color properties are hex codes
        assert colors.primary_start.startswith("#")
        assert colors.primary_end.startswith("#")
        assert colors.background_start.startswith("#")
        assert colors.background_end.startswith("#")
        assert colors.accent_color.startswith("#")
        assert colors.glow_color.startswith("#")
        
        # Check hex code format
        assert len(colors.primary_start) == 7
        assert len(colors.primary_end) == 7
    
    def test_visual_effects_generation(self, generator, sample_profile):
        """Test visual effects generation."""
        effects = generator.generate_visual_effects(sample_profile, "typewriter")
        
        assert 0 <= effects.glow_intensity <= 1
        assert effects.animation_speed > 0
        assert effects.blur_radius >= 0
        assert 0 <= effects.gradient_angle <= 360
        assert 0 <= effects.shadow_intensity <= 1


class TestCSSGenerator:
    """Test CSS generation functionality."""
    
    @pytest.fixture
    def generator(self):
        return CSSGenerator()
    
    @pytest.fixture
    def sample_theme(self):
        from emotional_decoration.models import ThemeConfig, ColorScheme, VisualEffect
        
        colors = ColorScheme(
            primary_start="#4A90E2",
            primary_end="#7ED321",
            background_start="#000428",
            background_end="#004e92",
            accent_color="#50E3C2",
            glow_color="#4A90E2"
        )
        
        effects = VisualEffect(
            glow_intensity=0.5,
            animation_speed=1.0,
            blur_radius=1.0,
            pulse_enabled=True,
            gradient_angle=45,
            shadow_enabled=True,
            shadow_intensity=0.5
        )
        
        return ThemeConfig(
            name="Test Theme",
            description="A test theme for unit testing",
            colors=colors,
            effects=effects,
            typography={"font_weight": "normal"},
            compatibility=["typewriter"]
        )
    
    def test_css_generation(self, generator, sample_theme):
        """Test CSS generation."""
        css = generator.generate_css(sample_theme, "typewriter")
        
        assert css is not None
        assert len(css) > 0
        
        # Check for CSS custom properties
        assert "--decoration-primary-start" in css
        assert "--decoration-primary-end" in css
        assert "--decoration-glow-intensity" in css
        
        # Check for CSS rules
        assert ".typewriter-char" in css
        assert "linear-gradient" in css
        assert "background-clip" in css
    
    def test_css_minification(self, generator, sample_theme):
        """Test CSS minification."""
        normal_css = generator.generate_css(sample_theme, "typewriter")
        minified_css = generator.generate_minified_css(sample_theme, "typewriter")
        
        assert len(minified_css) < len(normal_css)
        assert "/*" not in minified_css  # Comments removed
        assert "  " not in minified_css  # Extra spaces removed
    
    def test_template_compatibility(self, generator, sample_theme):
        """Test CSS generation for different templates."""
        templates = ["typewriter", "railway", "scroll"]
        
        for template in templates:
            css = generator.generate_css(sample_theme, template)
            assert css is not None
            assert len(css) > 0
            
            # Should contain template-specific or generic selectors
            has_template_selector = (
                f".{template}-" in css or 
                ".typewriter-" in css or
                "decoration-enhanced" in css
            )
            assert has_template_selector


class TestErrorHandling:
    """Test error handling across components."""
    
    def test_empty_text_handling(self):
        """Test handling of empty text input."""
        analyzer = ContentAnalyzer()
        
        result = analyzer.analyze("")
        assert result is not None
        assert result.word_count == 0
        assert result.character_count == 0
    
    def test_invalid_theme_handling(self):
        """Test handling of invalid theme configurations."""
        generator = ThemeGenerator()
        
        # Test with minimal profile
        minimal_profile = ContentProfile(
            emotion=EmotionType.NEUTRAL,
            content_type=ContentType.PROFESSIONAL,
            difficulty=DifficultyLevel.MEDIUM,
            emotion_intensity=0.0,
            reading_speed=250.0,
            recommended_theme="nonexistent_theme",
            confidence=0.0
        )
        
        # Should not crash
        theme = generator.generate_theme(minimal_profile)
        assert theme is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])