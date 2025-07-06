"""Content analysis pipeline for emotional-decoration system."""

import time
from typing import Dict, List, Optional
from ..models import (
    ContentProfile, AnalysisResult, EmotionType, ContentType, DifficultyLevel
)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from analyzers.emotion_detector import EmotionDetector
from analyzers.content_classifier import ContentClassifier


class ContentAnalyzer:
    """Main content analysis pipeline integrating emotion detection and content classification."""
    
    def __init__(self):
        self.emotion_detector = EmotionDetector()
        self.content_classifier = ContentClassifier()
        self.analysis_cache: Dict[str, AnalysisResult] = {}
        
    def analyze(self, text: str, use_cache: bool = True) -> AnalysisResult:
        """
        Perform comprehensive content analysis.
        
        Args:
            text: Input text to analyze
            use_cache: Whether to use cached results for identical text
            
        Returns:
            AnalysisResult containing complete analysis
        """
        start_time = time.time()
        
        # Check cache first
        if use_cache and text in self.analysis_cache:
            cached_result = self.analysis_cache[text]
            # Update processing time to reflect cache hit
            cached_result.processing_time = time.time() - start_time
            return cached_result
        
        # Basic text metrics
        words = text.split()
        sentences = self._split_sentences(text)
        word_count = len(words)
        character_count = len(text)
        
        # Emotion analysis
        primary_emotion, emotion_intensity = self.emotion_detector.detect_emotion(text)
        
        # Content classification
        content_type, content_confidence = self.content_classifier.classify_content(text)
        
        # Difficulty assessment
        difficulty = self._assess_difficulty(text)
        
        # Reading speed estimation
        reading_speed = self._estimate_reading_speed(text, content_type)
        
        # Key themes extraction
        key_themes = self._extract_key_themes(text)
        
        # Recommended theme determination
        recommended_theme = self._determine_recommended_theme(
            primary_emotion, content_type, difficulty
        )
        
        # Create content profile
        profile = ContentProfile(
            emotion=primary_emotion,
            content_type=content_type,
            difficulty=difficulty,
            emotion_intensity=emotion_intensity,
            reading_speed=reading_speed,
            key_themes=key_themes,
            recommended_theme=recommended_theme,
            confidence=content_confidence
        )
        
        # Extract keywords
        keywords = self._extract_keywords(text)
        
        # Create analysis result
        processing_time = time.time() - start_time
        result = AnalysisResult(
            text=text,
            profile=profile,
            processing_time=processing_time,
            word_count=word_count,
            character_count=character_count,
            sentences=sentences,
            keywords=keywords
        )
        
        # Cache result
        if use_cache:
            self.analysis_cache[text] = result
        
        return result
    
    def analyze_batch(self, texts: List[str], use_cache: bool = True) -> List[AnalysisResult]:
        """
        Analyze multiple texts in batch.
        
        Args:
            texts: List of texts to analyze
            use_cache: Whether to use cached results
            
        Returns:
            List of AnalysisResult objects
        """
        return [self.analyze(text, use_cache) for text in texts]
    
    def get_analysis_summary(self, result: AnalysisResult) -> Dict[str, any]:
        """
        Get a summary of analysis results.
        
        Args:
            result: Analysis result to summarize
            
        Returns:
            Dictionary with key analysis metrics
        """
        return {
            'text_length': result.character_count,
            'word_count': result.word_count,
            'sentence_count': len(result.sentences),
            'primary_emotion': result.profile.emotion.value,
            'emotion_intensity': result.profile.emotion_intensity,
            'content_type': result.profile.content_type.value,
            'difficulty': result.profile.difficulty.value,
            'reading_speed': result.profile.reading_speed,
            'recommended_theme': result.profile.recommended_theme,
            'confidence': result.profile.confidence,
            'processing_time': result.processing_time,
            'key_themes': result.profile.key_themes,
            'keywords': result.keywords[:10]  # Top 10 keywords
        }
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _assess_difficulty(self, text: str) -> DifficultyLevel:
        """Assess reading difficulty based on text complexity."""
        complexity_metrics = self.content_classifier.analyze_complexity(text)
        
        avg_word_length = complexity_metrics['avg_word_length']
        avg_sentence_length = complexity_metrics['avg_sentence_length']
        vocabulary_richness = complexity_metrics['vocabulary_richness']
        
        # Calculate difficulty score
        difficulty_score = (
            (avg_word_length - 4) * 0.3 +
            (avg_sentence_length - 15) * 0.02 +
            (vocabulary_richness - 0.5) * 0.5
        )
        
        if difficulty_score < -0.3:
            return DifficultyLevel.EASY
        elif difficulty_score < 0.1:
            return DifficultyLevel.MEDIUM
        elif difficulty_score < 0.4:
            return DifficultyLevel.HARD
        else:
            return DifficultyLevel.EXPERT
    
    def _estimate_reading_speed(self, text: str, content_type: ContentType) -> float:
        """Estimate reading speed based on content type and complexity."""
        base_speed = 250  # words per minute
        
        # Adjust based on content type
        speed_modifiers = {
            ContentType.LEARNING: 0.8,      # Slower for educational content
            ContentType.ENTERTAINMENT: 1.2,  # Faster for entertainment
            ContentType.NARRATIVE: 1.0,     # Normal for stories
            ContentType.PROFESSIONAL: 0.9,  # Slightly slower for business
            ContentType.TECHNICAL: 0.7,     # Much slower for technical
            ContentType.CREATIVE: 1.1       # Slightly faster for creative
        }
        
        return base_speed * speed_modifiers.get(content_type, 1.0)
    
    def _extract_key_themes(self, text: str) -> List[str]:
        """Extract key themes from text."""
        # Get content distribution to understand mixed themes
        content_dist = self.content_classifier.get_content_distribution(text)
        emotion_dist = self.emotion_detector.get_emotion_distribution(text)
        
        themes = []
        
        # Add content-based themes
        for content_type, score in content_dist.items():
            if score > 0.2:  # Threshold for significant presence
                themes.append(content_type.value)
        
        # Add emotion-based themes
        for emotion, score in emotion_dist.items():
            if score > 0.2:
                themes.append(f"{emotion.value}_emotion")
        
        return themes[:5]  # Return top 5 themes
    
    def _determine_recommended_theme(
        self, 
        emotion: EmotionType, 
        content_type: ContentType, 
        difficulty: DifficultyLevel
    ) -> str:
        """Determine recommended visual theme based on analysis."""
        
        # Primary theme based on content type
        if content_type == ContentType.LEARNING:
            base_theme = "learning"
        elif content_type == ContentType.PROFESSIONAL:
            base_theme = "professional"
        elif content_type in [ContentType.NARRATIVE, ContentType.CREATIVE]:
            base_theme = "emotional"
        else:
            base_theme = "professional"  # Default
        
        # Modify based on emotion intensity and type
        if emotion in [EmotionType.EXCITED, EmotionType.HAPPY]:
            if base_theme == "learning":
                return "learning_energetic"
            elif base_theme == "professional":
                return "professional_positive"
            else:
                return "emotional_vibrant"
        elif emotion in [EmotionType.CALM, EmotionType.NEUTRAL]:
            if base_theme == "learning":
                return "learning_focused"
            elif base_theme == "professional":
                return "professional_minimal"
            else:
                return "emotional_serene"
        elif emotion in [EmotionType.SAD, EmotionType.FEARFUL]:
            if base_theme == "learning":
                return "learning_supportive"
            elif base_theme == "professional":
                return "professional_subtle"
            else:
                return "emotional_contemplative"
        
        # Adjust for difficulty
        if difficulty == DifficultyLevel.EXPERT:
            return f"{base_theme}_sophisticated"
        elif difficulty == DifficultyLevel.EASY:
            return f"{base_theme}_accessible"
        
        return base_theme
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text."""
        import re
        from collections import Counter
        
        # Clean and tokenize
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i',
            'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        # Filter words
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count frequency and return top keywords
        word_counts = Counter(filtered_words)
        return [word for word, count in word_counts.most_common(20)]
    
    def clear_cache(self):
        """Clear the analysis cache."""
        self.analysis_cache.clear()
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            'cache_size': len(self.analysis_cache),
            'total_cached_chars': sum(len(text) for text in self.analysis_cache.keys())
        }