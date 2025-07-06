"""Content type classification from text analysis."""

import re
from typing import Dict, List, Set, Tuple
from collections import Counter

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent / "src"))
from emotional_decoration.models import ContentType


class ContentClassifier:
    """Classifies content type based on text analysis."""
    
    def __init__(self):
        self.content_indicators = {
            ContentType.LEARNING: {
                'keywords': [
                    'learn', 'study', 'understand', 'explain', 'tutorial', 'lesson',
                    'chapter', 'concept', 'definition', 'example', 'exercise',
                    'practice', 'knowledge', 'education', 'research', 'analysis',
                    'theory', 'principle', 'method', 'technique', 'skill',
                    'development', 'improvement', 'mastery', 'fundamentals'
                ],
                'patterns': [
                    r'\b(?:how to|learn|understand|explain)\b',
                    r'\b(?:step \d+|first|second|third|finally)\b',
                    r'\b(?:in conclusion|to summarize|key points)\b',
                    r'\b(?:for example|such as|including)\b'
                ],
                'structures': [
                    'numbered_lists',
                    'instructional_language',
                    'explanatory_phrases'
                ]
            },
            ContentType.ENTERTAINMENT: {
                'keywords': [
                    'fun', 'exciting', 'adventure', 'story', 'movie', 'game',
                    'music', 'dance', 'party', 'celebration', 'humor', 'comedy',
                    'laugh', 'entertainment', 'show', 'performance', 'video',
                    'social', 'friends', 'enjoy', 'amazing', 'awesome', 'cool'
                ],
                'patterns': [
                    r'\b(?:haha|lol|omg|wow)\b',
                    r'\b(?:check this out|look at this|amazing)\b',
                    r'\b(?:so funny|hilarious|incredible)\b',
                    r'[!]{2,}|[?]{2,}'
                ],
                'structures': [
                    'exclamatory_language',
                    'casual_tone',
                    'social_expressions'
                ]
            },
            ContentType.NARRATIVE: {
                'keywords': [
                    'story', 'tale', 'character', 'plot', 'journey', 'adventure',
                    'once', 'began', 'happened', 'told', 'narrative', 'chapter',
                    'episode', 'scene', 'dialogue', 'description', 'setting',
                    'conflict', 'resolution', 'climax', 'protagonist', 'antagonist'
                ],
                'patterns': [
                    r'\b(?:once upon a time|in the beginning|long ago)\b',
                    r'\b(?:he said|she said|they said)\b',
                    r'\b(?:suddenly|meanwhile|later|finally)\b',
                    r'\b(?:the end|to be continued)\b'
                ],
                'structures': [
                    'temporal_sequences',
                    'character_dialogue',
                    'descriptive_language'
                ]
            },
            ContentType.PROFESSIONAL: {
                'keywords': [
                    'business', 'company', 'strategy', 'management', 'team',
                    'project', 'meeting', 'client', 'customer', 'service',
                    'solution', 'analysis', 'report', 'proposal', 'budget',
                    'revenue', 'profit', 'growth', 'market', 'industry',
                    'professional', 'corporate', 'organization', 'department'
                ],
                'patterns': [
                    r'\b(?:Q\d+|FY\d+|KPI|ROI|CEO|CFO|CTO)\b',
                    r'\b(?:please find|attached|regarding|pursuant to)\b',
                    r'\b(?:best regards|sincerely|respectfully)\b',
                    r'\$[\d,]+\.?\d*'
                ],
                'structures': [
                    'formal_language',
                    'business_terminology',
                    'structured_format'
                ]
            },
            ContentType.TECHNICAL: {
                'keywords': [
                    'system', 'software', 'hardware', 'code', 'programming',
                    'development', 'algorithm', 'database', 'server', 'network',
                    'security', 'protocol', 'framework', 'library', 'api',
                    'function', 'variable', 'parameter', 'configuration', 'debug',
                    'implementation', 'deployment', 'architecture', 'engineering'
                ],
                'patterns': [
                    r'\b(?:var|const|function|class|import|export)\b',
                    r'\b(?:HTTP|API|SQL|JSON|XML|CSS|HTML)\b',
                    r'\b(?:version \d+|v\d+\.\d+)\b',
                    r'[a-zA-Z_][a-zA-Z0-9_]*\(\)'
                ],
                'structures': [
                    'code_snippets',
                    'technical_terminology',
                    'precise_language'
                ]
            },
            ContentType.CREATIVE: {
                'keywords': [
                    'art', 'creative', 'design', 'beautiful', 'inspiration',
                    'imagination', 'expression', 'artistic', 'aesthetic', 'style',
                    'color', 'form', 'composition', 'texture', 'visual', 'audio',
                    'poetry', 'music', 'painting', 'sculpture', 'photography',
                    'writing', 'creation', 'innovation', 'unique', 'original'
                ],
                'patterns': [
                    r'\b(?:imagine|visualize|picture this|envision)\b',
                    r'\b(?:artistic|creative|innovative|unique)\b',
                    r'\b(?:colors|shapes|forms|textures)\b',
                    r'[~]+|[*]+.*[*]+'
                ],
                'structures': [
                    'descriptive_language',
                    'metaphorical_expressions',
                    'sensory_descriptions'
                ]
            }
        }
        
        self.structural_patterns = {
            'numbered_lists': r'^\s*\d+[\.\)]\s+',
            'bullet_points': r'^\s*[•\-\*]\s+',
            'questions': r'\?',
            'exclamations': r'!',
            'quotes': r'["\'].*["\']',
            'code_blocks': r'```|`.*`',
            'urls': r'https?://\S+',
            'hashtags': r'#\w+',
            'mentions': r'@\w+'
        }
    
    def classify_content(self, text: str) -> Tuple[ContentType, float]:
        """
        Classify content type and return confidence score.
        
        Args:
            text: Input text to classify
            
        Returns:
            Tuple of (content_type, confidence_score)
        """
        if not text or not text.strip():
            return ContentType.PROFESSIONAL, 0.0
        
        # Calculate scores for each content type
        scores = self._calculate_content_scores(text)
        
        # Apply structural analysis
        structural_boost = self._analyze_structure(text)
        
        # Combine scores
        for content_type in scores:
            scores[content_type] *= structural_boost.get(content_type, 1.0)
        
        # Determine primary content type
        if not scores or max(scores.values()) == 0:
            return ContentType.PROFESSIONAL, 0.0
        
        primary_type = max(scores, key=scores.get)
        max_score = scores[primary_type]
        
        # Calculate confidence based on score dominance
        total_score = sum(scores.values())
        confidence = max_score / total_score if total_score > 0 else 0.0
        
        return primary_type, confidence
    
    def get_content_distribution(self, text: str) -> Dict[ContentType, float]:
        """
        Get distribution of content type scores.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary mapping content types to their scores
        """
        if not text or not text.strip():
            return {content_type: 0.0 for content_type in ContentType}
        
        scores = self._calculate_content_scores(text)
        structural_boost = self._analyze_structure(text)
        
        # Apply structural analysis
        for content_type in scores:
            scores[content_type] *= structural_boost.get(content_type, 1.0)
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v / total_score for k, v in scores.items()}
        
        return scores
    
    def _calculate_content_scores(self, text: str) -> Dict[ContentType, float]:
        """Calculate base content type scores."""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        word_count = len(words)
        
        scores = {content_type: 0.0 for content_type in ContentType}
        
        for content_type, indicators in self.content_indicators.items():
            # Keyword matching
            keyword_score = 0.0
            for keyword in indicators['keywords']:
                keyword_count = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text_lower))
                keyword_score += keyword_count
            
            # Pattern matching
            pattern_score = 0.0
            for pattern in indicators['patterns']:
                matches = len(re.findall(pattern, text_lower, re.IGNORECASE))
                pattern_score += matches * 2  # Patterns are weighted higher
            
            # Combine scores and normalize by text length
            total_score = keyword_score + pattern_score
            scores[content_type] = total_score / max(word_count, 1)
        
        return scores
    
    def _analyze_structure(self, text: str) -> Dict[ContentType, float]:
        """Analyze text structure for content type hints."""
        boost = {content_type: 1.0 for content_type in ContentType}
        
        # Check for numbered lists (learning content)
        if re.search(self.structural_patterns['numbered_lists'], text, re.MULTILINE):
            boost[ContentType.LEARNING] *= 1.3
            boost[ContentType.PROFESSIONAL] *= 1.1
        
        # Check for bullet points
        if re.search(self.structural_patterns['bullet_points'], text, re.MULTILINE):
            boost[ContentType.PROFESSIONAL] *= 1.2
            boost[ContentType.LEARNING] *= 1.1
        
        # Check for questions (interactive/learning content)
        question_count = len(re.findall(self.structural_patterns['questions'], text))
        if question_count > 0:
            question_ratio = question_count / len(text.split('.'))
            if question_ratio > 0.2:
                boost[ContentType.LEARNING] *= 1.2
                boost[ContentType.ENTERTAINMENT] *= 1.1
        
        # Check for exclamations (entertainment/emotional content)
        exclamation_count = len(re.findall(self.structural_patterns['exclamations'], text))
        if exclamation_count > 0:
            exclamation_ratio = exclamation_count / len(text.split())
            if exclamation_ratio > 0.05:
                boost[ContentType.ENTERTAINMENT] *= 1.3
                boost[ContentType.CREATIVE] *= 1.2
        
        # Check for quotes (narrative content)
        if re.search(self.structural_patterns['quotes'], text):
            boost[ContentType.NARRATIVE] *= 1.2
            boost[ContentType.CREATIVE] *= 1.1
        
        # Check for code blocks (technical content)
        if re.search(self.structural_patterns['code_blocks'], text):
            boost[ContentType.TECHNICAL] *= 1.5
        
        # Check for social media patterns
        if (re.search(self.structural_patterns['hashtags'], text) or
            re.search(self.structural_patterns['mentions'], text)):
            boost[ContentType.ENTERTAINMENT] *= 1.2
            boost[ContentType.CREATIVE] *= 1.1
        
        # Check for URLs (technical/professional content)
        if re.search(self.structural_patterns['urls'], text):
            boost[ContentType.TECHNICAL] *= 1.1
            boost[ContentType.PROFESSIONAL] *= 1.1
        
        return boost
    
    def analyze_complexity(self, text: str) -> Dict[str, float]:
        """
        Analyze text complexity metrics.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with complexity metrics
        """
        words = re.findall(r'\b\w+\b', text.lower())
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not words or not sentences:
            return {
                'avg_word_length': 0.0,
                'avg_sentence_length': 0.0,
                'vocabulary_richness': 0.0,
                'readability_score': 0.0
            }
        
        # Average word length
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Average sentence length
        avg_sentence_length = len(words) / len(sentences)
        
        # Vocabulary richness (unique words / total words)
        unique_words = set(words)
        vocabulary_richness = len(unique_words) / len(words)
        
        # Simple readability score (based on sentence and word length)
        readability_score = max(0, min(1, 1 - (avg_sentence_length * 0.02 + avg_word_length * 0.1 - 0.5)))
        
        return {
            'avg_word_length': avg_word_length,
            'avg_sentence_length': avg_sentence_length,
            'vocabulary_richness': vocabulary_richness,
            'readability_score': readability_score
        }