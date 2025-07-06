"""Emotion detection from text content."""

import re
from typing import Dict, List, Tuple

# Try to import TextBlob, fall back to basic sentiment if not available
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from emotional_decoration.models import EmotionType


class EmotionDetector:
    """Detects emotional tone from text content."""
    
    def __init__(self):
        self.emotion_keywords = {
            EmotionType.HAPPY: [
                'happy', 'joy', 'excited', 'wonderful', 'amazing', 'great', 'fantastic',
                'awesome', 'brilliant', 'excellent', 'love', 'celebrate', 'success',
                'achievement', 'victory', 'smile', 'laugh', 'cheerful', 'delighted'
            ],
            EmotionType.SAD: [
                'sad', 'sorrow', 'grief', 'depressed', 'unhappy', 'melancholy',
                'disappointed', 'heartbroken', 'tragedy', 'loss', 'cry', 'tears',
                'pain', 'hurt', 'lonely', 'empty', 'despair', 'misery'
            ],
            EmotionType.EXCITED: [
                'excited', 'thrilled', 'energetic', 'enthusiastic', 'passionate',
                'eager', 'pumped', 'animated', 'dynamic', 'vibrant', 'electric',
                'intense', 'fired up', 'exhilarated', 'rush', 'adrenaline'
            ],
            EmotionType.CALM: [
                'calm', 'peaceful', 'serene', 'tranquil', 'relaxed', 'gentle',
                'quiet', 'still', 'meditation', 'zen', 'balance', 'harmony',
                'soothing', 'comfortable', 'stable', 'centered', 'mindful'
            ],
            EmotionType.ANGRY: [
                'angry', 'rage', 'furious', 'mad', 'irritated', 'frustrated',
                'annoyed', 'outraged', 'livid', 'hate', 'aggravated', 'hostile',
                'resentful', 'bitter', 'explosive', 'fierce', 'aggressive'
            ],
            EmotionType.FEARFUL: [
                'fear', 'afraid', 'scared', 'terrified', 'anxious', 'worried',
                'nervous', 'panic', 'dread', 'horror', 'frightened', 'alarmed',
                'concerned', 'uneasy', 'apprehensive', 'timid', 'insecure'
            ],
            EmotionType.SURPRISED: [
                'surprised', 'amazed', 'astonished', 'shocked', 'stunned',
                'bewildered', 'confused', 'unexpected', 'sudden', 'wow',
                'incredible', 'unbelievable', 'extraordinary', 'remarkable'
            ]
        }
        
        self.intensity_modifiers = {
            'very': 1.3,
            'extremely': 1.5,
            'incredibly': 1.4,
            'absolutely': 1.3,
            'completely': 1.2,
            'totally': 1.2,
            'quite': 1.1,
            'really': 1.2,
            'so': 1.1,
            'rather': 0.9,
            'somewhat': 0.8,
            'slightly': 0.7,
            'a bit': 0.6,
            'a little': 0.6
        }
    
    def detect_emotion(self, text: str) -> Tuple[EmotionType, float]:
        """
        Detect primary emotion and intensity from text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Tuple of (emotion_type, intensity_score)
        """
        if not text or not text.strip():
            return EmotionType.NEUTRAL, 0.0
        
        # Clean and prepare text
        clean_text = self._clean_text(text)
        words = clean_text.lower().split()
        
        # Calculate emotion scores
        emotion_scores = self._calculate_emotion_scores(words)
        
        # Apply sentiment analysis
        sentiment_boost = self._get_sentiment_boost(text)
        
        # Apply intensity modifiers
        emotion_scores = self._apply_intensity_modifiers(emotion_scores, words)
        
        # Add sentiment boost
        for emotion in emotion_scores:
            emotion_scores[emotion] *= sentiment_boost.get(emotion, 1.0)
        
        # Determine primary emotion
        if not emotion_scores or max(emotion_scores.values()) == 0:
            return EmotionType.NEUTRAL, 0.0
        
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        max_score = emotion_scores[primary_emotion]
        
        # Normalize intensity score
        intensity = min(max_score / len(words), 1.0) if words else 0.0
        
        return primary_emotion, intensity
    
    def get_emotion_distribution(self, text: str) -> Dict[EmotionType, float]:
        """
        Get distribution of all emotions in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary mapping emotions to their scores
        """
        if not text or not text.strip():
            return {emotion: 0.0 for emotion in EmotionType}
        
        clean_text = self._clean_text(text)
        words = clean_text.lower().split()
        
        emotion_scores = self._calculate_emotion_scores(words)
        emotion_scores = self._apply_intensity_modifiers(emotion_scores, words)
        
        # Normalize scores
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            emotion_scores = {k: v / total_score for k, v in emotion_scores.items()}
        
        # Ensure all emotions are present
        for emotion in EmotionType:
            if emotion not in emotion_scores:
                emotion_scores[emotion] = 0.0
        
        return emotion_scores
    
    def _clean_text(self, text: str) -> str:
        """Clean text for analysis."""
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove special characters but keep apostrophes
        text = re.sub(r'[^\w\s\']', ' ', text)
        return text
    
    def _calculate_emotion_scores(self, words: List[str]) -> Dict[EmotionType, float]:
        """Calculate base emotion scores from keywords."""
        emotion_scores = {emotion: 0.0 for emotion in self.emotion_keywords}
        
        for word in words:
            for emotion, keywords in self.emotion_keywords.items():
                if word in keywords:
                    emotion_scores[emotion] += 1.0
                # Check for partial matches
                elif any(keyword in word or word in keyword for keyword in keywords):
                    emotion_scores[emotion] += 0.5
        
        return emotion_scores
    
    def _apply_intensity_modifiers(
        self, 
        emotion_scores: Dict[EmotionType, float], 
        words: List[str]
    ) -> Dict[EmotionType, float]:
        """Apply intensity modifiers to emotion scores."""
        modified_scores = emotion_scores.copy()
        
        for i, word in enumerate(words):
            if word in self.intensity_modifiers:
                modifier = self.intensity_modifiers[word]
                # Apply to next few words
                for j in range(i + 1, min(i + 4, len(words))):
                    next_word = words[j]
                    for emotion, keywords in self.emotion_keywords.items():
                        if next_word in keywords:
                            modified_scores[emotion] *= modifier
        
        return modified_scores
    
    def _get_sentiment_boost(self, text: str) -> Dict[EmotionType, float]:
        """Get sentiment analysis boost for emotions."""
        try:
            if TEXTBLOB_AVAILABLE:
                blob = TextBlob(text)
                polarity = blob.sentiment.polarity  # -1 to 1
                subjectivity = blob.sentiment.subjectivity  # 0 to 1
            else:
                # Simple fallback sentiment analysis
                positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'love', 'happy', 'joy']
                negative_words = ['bad', 'terrible', 'awful', 'hate', 'sad', 'angry', 'fear', 'worry']
                
                words = text.lower().split()
                positive_count = sum(1 for word in words if word in positive_words)
                negative_count = sum(1 for word in words if word in negative_words)
                
                total_sentiment_words = positive_count + negative_count
                if total_sentiment_words == 0:
                    polarity = 0.0
                else:
                    polarity = (positive_count - negative_count) / len(words)
                
                subjectivity = min(total_sentiment_words / len(words), 1.0) if words else 0.0
            
            boost = {emotion: 1.0 for emotion in EmotionType}
            
            if polarity > 0.1:  # Positive sentiment
                boost[EmotionType.HAPPY] = 1.0 + polarity * 0.5
                boost[EmotionType.EXCITED] = 1.0 + polarity * 0.3
                boost[EmotionType.SAD] = 1.0 - polarity * 0.3
                boost[EmotionType.ANGRY] = 1.0 - polarity * 0.3
                boost[EmotionType.FEARFUL] = 1.0 - polarity * 0.2
            elif polarity < -0.1:  # Negative sentiment
                boost[EmotionType.SAD] = 1.0 + abs(polarity) * 0.5
                boost[EmotionType.ANGRY] = 1.0 + abs(polarity) * 0.4
                boost[EmotionType.FEARFUL] = 1.0 + abs(polarity) * 0.3
                boost[EmotionType.HAPPY] = 1.0 - abs(polarity) * 0.4
                boost[EmotionType.EXCITED] = 1.0 - abs(polarity) * 0.3
            
            # High subjectivity boosts emotional content
            if subjectivity > 0.5:
                emotion_boost = 1.0 + (subjectivity - 0.5) * 0.3
                for emotion in [EmotionType.HAPPY, EmotionType.SAD, EmotionType.EXCITED, 
                               EmotionType.ANGRY, EmotionType.FEARFUL]:
                    boost[emotion] *= emotion_boost
            
            return boost
            
        except Exception:
            return {emotion: 1.0 for emotion in EmotionType}
    
    def analyze_emotional_journey(self, text: str, segment_size: int = 50) -> List[Tuple[EmotionType, float]]:
        """
        Analyze emotional journey through text segments.
        
        Args:
            text: Input text to analyze
            segment_size: Number of words per segment
            
        Returns:
            List of (emotion, intensity) tuples for each segment
        """
        words = text.split()
        segments = []
        
        for i in range(0, len(words), segment_size):
            segment = ' '.join(words[i:i + segment_size])
            emotion, intensity = self.detect_emotion(segment)
            segments.append((emotion, intensity))
        
        return segments