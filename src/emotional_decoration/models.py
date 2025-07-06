"""Data models for emotional-decoration system."""

from typing import Dict, List, Optional, Any, Tuple
from pydantic import BaseModel, Field
from enum import Enum


class EmotionType(str, Enum):
    """Detected emotion types."""
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    CALM = "calm"
    ANGRY = "angry"
    FEARFUL = "fearful"
    SURPRISED = "surprised"
    NEUTRAL = "neutral"


class ContentType(str, Enum):
    """Content classification types."""
    LEARNING = "learning"
    ENTERTAINMENT = "entertainment"
    NARRATIVE = "narrative"
    PROFESSIONAL = "professional"
    TECHNICAL = "technical"
    CREATIVE = "creative"


class DifficultyLevel(str, Enum):
    """Reading difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class ContentProfile(BaseModel):
    """Content analysis profile."""
    emotion: EmotionType
    content_type: ContentType
    difficulty: DifficultyLevel
    emotion_intensity: float = Field(ge=0.0, le=1.0)
    reading_speed: float = Field(gt=0.0)
    key_themes: List[str] = Field(default_factory=list)
    recommended_theme: str
    confidence: float = Field(ge=0.0, le=1.0)
    
    class Config:
        json_encoders = {
            EmotionType: lambda v: v.value,
            ContentType: lambda v: v.value,
            DifficultyLevel: lambda v: v.value,
        }


class ColorScheme(BaseModel):
    """Color scheme for visual enhancement."""
    primary_start: str = Field(pattern=r'^#[0-9A-Fa-f]{6}$')
    primary_end: str = Field(pattern=r'^#[0-9A-Fa-f]{6}$')
    background_start: str = Field(pattern=r'^#[0-9A-Fa-f]{6}$')
    background_end: str = Field(pattern=r'^#[0-9A-Fa-f]{6}$')
    accent_color: str = Field(pattern=r'^#[0-9A-Fa-f]{6}$')
    glow_color: str = Field(pattern=r'^#[0-9A-Fa-f]{6}$')
    
    @property
    def primary_rgba(self) -> Tuple[int, int, int, float]:
        """Convert primary color to RGBA."""
        return self._hex_to_rgba(self.primary_start)
    
    @property
    def glow_rgba(self) -> Tuple[int, int, int, float]:
        """Convert glow color to RGBA with transparency."""
        r, g, b, _ = self._hex_to_rgba(self.glow_color)
        return (r, g, b, 0.3)
    
    def _hex_to_rgba(self, hex_color: str) -> Tuple[int, int, int, float]:
        """Convert hex color to RGBA tuple."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (1.0,)


class VisualEffect(BaseModel):
    """Visual effect configuration."""
    glow_intensity: float = Field(ge=0.0, le=1.0, default=0.3)
    animation_speed: float = Field(gt=0.0, default=1.0)
    blur_radius: float = Field(ge=0.0, default=0.0)
    pulse_enabled: bool = False
    gradient_angle: int = Field(ge=0, le=360, default=45)
    shadow_enabled: bool = True
    shadow_intensity: float = Field(ge=0.0, le=1.0, default=0.5)


class ThemeConfig(BaseModel):
    """Theme configuration."""
    name: str
    description: str
    colors: ColorScheme
    effects: VisualEffect
    typography: Dict[str, Any] = Field(default_factory=dict)
    compatibility: List[str] = Field(default_factory=list)  # Compatible scroll-cast templates


class DecorationOutput(BaseModel):
    """Generated decoration output."""
    css_content: str
    js_content: Optional[str] = None
    theme_config: ThemeConfig
    manifest: Dict[str, Any] = Field(default_factory=dict)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)


class AnalysisResult(BaseModel):
    """Text analysis result."""
    text: str
    profile: ContentProfile
    processing_time: float
    word_count: int
    character_count: int
    sentences: List[str]
    keywords: List[str] = Field(default_factory=list)
    
    class Config:
        json_encoders = {
            ContentProfile: lambda v: v.dict(),
        }


class DecorationRequest(BaseModel):
    """Request for decoration generation."""
    text: str
    template_type: str  # scroll-cast template type
    theme_preference: Optional[str] = None
    custom_colors: Optional[ColorScheme] = None
    effects_config: Optional[VisualEffect] = None
    output_format: str = "css"
    
    class Config:
        json_encoders = {
            ColorScheme: lambda v: v.dict() if v else None,
            VisualEffect: lambda v: v.dict() if v else None,
        }


class DecorationResponse(BaseModel):
    """Response from decoration generation."""
    request: DecorationRequest
    analysis: AnalysisResult
    output: DecorationOutput
    generation_time: float
    success: bool
    error_message: Optional[str] = None
    
    class Config:
        json_encoders = {
            DecorationRequest: lambda v: v.dict(),
            AnalysisResult: lambda v: v.dict(),
            DecorationOutput: lambda v: v.dict(),
        }