"""Main decoration engine orchestrating the entire emotional-decoration workflow."""

import time
from typing import Dict, List, Optional
from ..models import (
    DecorationRequest, DecorationResponse, AnalysisResult, 
    DecorationOutput, ContentProfile
)
from ..boxing.content_analyzer import ContentAnalyzer
from ..coloring.theme_generator import ThemeGenerator
from ..packing.css_generator import CSSGenerator
from ..rendering.decoration_renderer import DecorationRenderer
from ..rendering.html_injector import HTMLInjector


class DecorationEngine:
    """Main orchestrator for the emotional-decoration system."""
    
    def __init__(self, output_dir: str = "decorations"):
        # Initialize all layers
        self.content_analyzer = ContentAnalyzer()
        self.theme_generator = ThemeGenerator()
        self.css_generator = CSSGenerator()
        self.decoration_renderer = DecorationRenderer(output_dir)
        self.html_injector = HTMLInjector()
        
        # Performance tracking
        self.performance_stats = {
            'total_requests': 0,
            'total_processing_time': 0.0,
            'average_chars_per_second': 0.0
        }
    
    def process_decoration_request(self, request: DecorationRequest) -> DecorationResponse:
        """
        Process a complete decoration request through all layers.
        
        Args:
            request: Decoration request with text and preferences
            
        Returns:
            DecorationResponse with analysis, decoration, and metadata
        """
        start_time = time.time()
        
        try:
            # Phase 1: Boxing - Content Analysis
            analysis_result = self.content_analyzer.analyze(request.text)
            
            # Phase 2: Coloring - Theme Generation
            # Override with custom preferences if provided
            if request.theme_preference:
                analysis_result.profile.recommended_theme = request.theme_preference
            
            if request.custom_colors:
                # Create custom theme with provided colors
                theme_config = self._create_custom_theme(
                    analysis_result.profile, 
                    request.custom_colors,
                    request.effects_config,
                    request.template_type
                )
            else:
                # Generate theme based on analysis
                theme_config = self.theme_generator.generate_theme(
                    analysis_result.profile, 
                    request.template_type
                )
            
            # Phase 3: Packing - CSS/JS Generation
            decoration_output = self.decoration_renderer.render_decoration(
                theme_config, 
                request.template_type
            )
            
            # Calculate processing metrics
            generation_time = time.time() - start_time
            
            # Update performance stats
            self._update_performance_stats(request.text, generation_time)
            
            # Create successful response
            response = DecorationResponse(
                request=request,
                analysis=analysis_result,
                output=decoration_output,
                generation_time=generation_time,
                success=True
            )
            
            return response
            
        except Exception as e:
            generation_time = time.time() - start_time
            
            # Create error response
            response = DecorationResponse(
                request=request,
                analysis=AnalysisResult(
                    text=request.text,
                    profile=ContentProfile(
                        emotion='neutral',
                        content_type='professional',
                        difficulty='medium',
                        emotion_intensity=0.0,
                        reading_speed=250.0,
                        recommended_theme='professional',
                        confidence=0.0
                    ),
                    processing_time=0.0,
                    word_count=len(request.text.split()),
                    character_count=len(request.text),
                    sentences=[],
                    keywords=[]
                ),
                output=DecorationOutput(
                    css_content="",
                    theme_config=theme_config if 'theme_config' in locals() else None,
                    manifest={}
                ),
                generation_time=generation_time,
                success=False,
                error_message=str(e)
            )
            
            return response
    
    def analyze_text(self, text: str) -> AnalysisResult:
        """
        Analyze text content without generating decoration.
        
        Args:
            text: Text to analyze
            
        Returns:
            AnalysisResult with content analysis
        """
        return self.content_analyzer.analyze(text)
    
    def generate_theme_only(
        self, 
        text: str, 
        template_type: str = "typewriter",
        theme_preference: Optional[str] = None
    ) -> DecorationOutput:
        """
        Generate theme and decoration without saving files.
        
        Args:
            text: Text to analyze
            template_type: Target scroll-cast template
            theme_preference: Optional theme preference
            
        Returns:
            DecorationOutput with generated theme
        """
        # Analyze content
        analysis_result = self.content_analyzer.analyze(text)
        
        # Override theme preference if provided
        if theme_preference:
            analysis_result.profile.recommended_theme = theme_preference
        
        # Generate theme
        theme_config = self.theme_generator.generate_theme(
            analysis_result.profile, 
            template_type
        )
        
        # Render decoration
        decoration_output = self.decoration_renderer.render_decoration(
            theme_config, 
            template_type
        )
        
        return decoration_output
    
    def enhance_html_file(
        self, 
        html_file: str, 
        text: str,
        output_file: Optional[str] = None,
        template_type: str = "typewriter",
        theme_preference: Optional[str] = None
    ) -> str:
        """
        Enhance an existing HTML file with emotional decoration.
        
        Args:
            html_file: Path to existing HTML file
            text: Text content for analysis
            output_file: Optional output file path
            template_type: scroll-cast template type
            theme_preference: Optional theme preference
            
        Returns:
            Path to enhanced HTML file
        """
        # Generate decoration
        decoration_output = self.generate_theme_only(
            text, 
            template_type, 
            theme_preference
        )
        
        # Inject decoration into HTML
        enhanced_file = self.html_injector.inject_decoration(
            html_file, 
            decoration_output, 
            output_file
        )
        
        return enhanced_file
    
    def save_decoration(
        self, 
        decoration_output: DecorationOutput, 
        name: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Save decoration output to files.
        
        Args:
            decoration_output: Decoration to save
            name: Optional custom name
            
        Returns:
            Dictionary mapping file types to paths
        """
        return self.decoration_renderer.save_decoration(decoration_output, name)
    
    def load_decoration(self, name: str) -> Optional[DecorationOutput]:
        """
        Load a saved decoration.
        
        Args:
            name: Name of decoration to load
            
        Returns:
            DecorationOutput if found, None otherwise
        """
        return self.decoration_renderer.load_decoration(name)
    
    def list_decorations(self) -> List[Dict[str, any]]:
        """
        List all available decorations.
        
        Returns:
            List of decoration metadata
        """
        return self.decoration_renderer.list_decorations()
    
    def delete_decoration(self, name: str) -> bool:
        """
        Delete a decoration and all its files.
        
        Args:
            name: Name of decoration to delete
            
        Returns:
            True if deleted successfully
        """
        return self.decoration_renderer.delete_decoration(name)
    
    def validate_html_compatibility(self, html_file: str) -> Dict[str, any]:
        """
        Validate HTML file compatibility with decoration system.
        
        Args:
            html_file: Path to HTML file
            
        Returns:
            Validation results
        """
        return self.html_injector.validate_html_structure(html_file)
    
    def preview_decoration(
        self, 
        html_file: str, 
        text: str,
        template_type: str = "typewriter",
        theme_preference: Optional[str] = None
    ) -> Dict[str, any]:
        """
        Preview decoration without applying it.
        
        Args:
            html_file: Path to HTML file
            text: Text content for analysis
            template_type: scroll-cast template type
            theme_preference: Optional theme preference
            
        Returns:
            Preview information
        """
        # Generate decoration
        decoration_output = self.generate_theme_only(
            text, 
            template_type, 
            theme_preference
        )
        
        # Generate preview
        preview = self.html_injector.preview_injection(html_file, decoration_output)
        
        # Add analysis information
        analysis_result = self.content_analyzer.analyze(text)
        preview['analysis'] = {
            'emotion': analysis_result.profile.emotion.value,
            'content_type': analysis_result.profile.content_type.value,
            'difficulty': analysis_result.profile.difficulty.value,
            'recommended_theme': analysis_result.profile.recommended_theme,
            'confidence': analysis_result.profile.confidence
        }
        
        return preview
    
    def get_performance_stats(self) -> Dict[str, any]:
        """
        Get system performance statistics.
        
        Returns:
            Performance metrics
        """
        return {
            **self.performance_stats,
            'cache_stats': self.content_analyzer.get_cache_stats(),
            'system_info': {
                'content_analyzer_initialized': self.content_analyzer is not None,
                'theme_generator_initialized': self.theme_generator is not None,
                'css_generator_initialized': self.css_generator is not None,
                'decoration_renderer_initialized': self.decoration_renderer is not None,
                'html_injector_initialized': self.html_injector is not None
            }
        }
    
    def clear_caches(self):
        """Clear all system caches."""
        self.content_analyzer.clear_cache()
        self.theme_generator.theme_cache.clear()
    
    def _create_custom_theme(
        self, 
        profile: ContentProfile, 
        custom_colors, 
        custom_effects,
        template_type: str
    ):
        """Create a custom theme with provided colors and effects."""
        from ..models import ThemeConfig, VisualEffect
        
        # Use custom colors or generate from profile
        colors = custom_colors or self.theme_generator.generate_color_scheme(profile)
        
        # Use custom effects or generate from profile
        if custom_effects:
            effects = custom_effects
        else:
            effects = self.theme_generator.generate_visual_effects(profile, template_type)
        
        # Generate typography
        typography = self.theme_generator._generate_typography(profile)
        
        return ThemeConfig(
            name=f"Custom {profile.emotion.value.title()} Theme",
            description=f"Custom theme for {profile.content_type.value} content",
            colors=colors,
            effects=effects,
            typography=typography,
            compatibility=[template_type]
        )
    
    def _update_performance_stats(self, text: str, processing_time: float):
        """Update system performance statistics."""
        char_count = len(text)
        
        self.performance_stats['total_requests'] += 1
        self.performance_stats['total_processing_time'] += processing_time
        
        # Calculate characters per second for this request
        chars_per_second = char_count / processing_time if processing_time > 0 else 0
        
        # Update running average
        total_requests = self.performance_stats['total_requests']
        current_avg = self.performance_stats['average_chars_per_second']
        
        self.performance_stats['average_chars_per_second'] = (
            (current_avg * (total_requests - 1) + chars_per_second) / total_requests
        )
    
    def create_batch_processor(self):
        """Create a batch processor for handling multiple requests efficiently."""
        return BatchProcessor(self)


class BatchProcessor:
    """Handles batch processing of decoration requests."""
    
    def __init__(self, engine: DecorationEngine):
        self.engine = engine
        
    def process_batch(self, requests: List[DecorationRequest]) -> List[DecorationResponse]:
        """
        Process multiple decoration requests in batch.
        
        Args:
            requests: List of decoration requests
            
        Returns:
            List of decoration responses
        """
        responses = []
        
        # Extract all text for batch analysis
        texts = [req.text for req in requests]
        analysis_results = self.engine.content_analyzer.analyze_batch(texts)
        
        # Process each request with pre-computed analysis
        for i, request in enumerate(requests):
            start_time = time.time()
            
            try:
                analysis_result = analysis_results[i]
                
                # Override with custom preferences
                if request.theme_preference:
                    analysis_result.profile.recommended_theme = request.theme_preference
                
                # Generate theme
                if request.custom_colors:
                    theme_config = self.engine._create_custom_theme(
                        analysis_result.profile,
                        request.custom_colors,
                        request.effects_config,
                        request.template_type
                    )
                else:
                    theme_config = self.engine.theme_generator.generate_theme(
                        analysis_result.profile,
                        request.template_type
                    )
                
                # Render decoration
                decoration_output = self.engine.decoration_renderer.render_decoration(
                    theme_config,
                    request.template_type
                )
                
                generation_time = time.time() - start_time
                
                response = DecorationResponse(
                    request=request,
                    analysis=analysis_result,
                    output=decoration_output,
                    generation_time=generation_time,
                    success=True
                )
                
            except Exception as e:
                generation_time = time.time() - start_time
                
                response = DecorationResponse(
                    request=request,
                    analysis=analysis_results[i] if i < len(analysis_results) else None,
                    output=DecorationOutput(css_content="", theme_config=None, manifest={}),
                    generation_time=generation_time,
                    success=False,
                    error_message=str(e)
                )
            
            responses.append(response)
        
        return responses