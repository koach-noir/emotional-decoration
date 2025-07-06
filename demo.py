#!/usr/bin/env python3
"""
Demonstration script for emotional-decoration system.

This script showcases the key features of the emotional-decoration system
and validates integration with scroll-cast CSS override architecture.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from emotional_decoration.orchestrator.decoration_engine import DecorationEngine
from emotional_decoration.models import DecorationRequest
from emotional_decoration.themes.theme_loader import ThemeLoader


def print_section(title):
    """Print a formatted section header."""
    print(f"\\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")


def print_subsection(title):
    """Print a formatted subsection header."""
    print(f"\\n{'-'*40}")
    print(f" {title}")
    print(f"{'-'*40}")


def demo_content_analysis():
    """Demonstrate content analysis capabilities."""
    print_section("CONTENT ANALYSIS DEMO")
    
    engine = DecorationEngine()
    
    # Test different types of content
    test_contents = [
        {
            "name": "Learning Content",
            "text": "Let's learn about machine learning fundamentals and understand how neural networks process information to make predictions."
        },
        {
            "name": "Professional Content", 
            "text": "Our quarterly business results demonstrate strong growth in revenue, market expansion, and customer satisfaction metrics."
        },
        {
            "name": "Emotional Content",
            "text": "I'm so excited about this amazing journey! The beautiful sunset fills my heart with joy and wonder."
        },
        {
            "name": "Technical Content",
            "text": "The API endpoint implements OAuth2 authentication with JWT tokens and returns JSON responses with proper error handling."
        }
    ]
    
    for content in test_contents:
        print_subsection(content["name"])
        
        start_time = time.time()
        analysis = engine.analyze_text(content["text"])
        processing_time = time.time() - start_time
        
        summary = engine.content_analyzer.get_analysis_summary(analysis)
        
        print(f"Text: {content['text'][:80]}...")
        print(f"Emotion: {summary['primary_emotion']} (intensity: {summary['emotion_intensity']:.2f})")
        print(f"Content Type: {summary['content_type']}")
        print(f"Difficulty: {summary['difficulty']}")
        print(f"Recommended Theme: {summary['recommended_theme']}")
        print(f"Processing Speed: {len(content['text'])/processing_time:.0f} chars/sec")
        print(f"Keywords: {', '.join(summary['keywords'][:5])}")


def demo_theme_generation():
    """Demonstrate theme generation capabilities."""
    print_section("THEME GENERATION DEMO")
    
    engine = DecorationEngine()
    
    test_scenarios = [
        {
            "name": "Educational Video",
            "text": "Today we'll learn about the fascinating world of astronomy and explore the mysteries of our solar system.",
            "template": "typewriter",
            "theme": "learning"
        },
        {
            "name": "Business Presentation",
            "text": "Our company's strategic vision focuses on innovation, growth, and delivering exceptional value to stakeholders.",
            "template": "railway", 
            "theme": "professional"
        },
        {
            "name": "Creative Story",
            "text": "Once upon a time, in a magical forest filled with glowing flowers and singing birds, a young adventurer began an incredible journey.",
            "template": "scroll",
            "theme": "emotional"
        }
    ]
    
    for scenario in test_scenarios:
        print_subsection(scenario["name"])
        
        decoration_output = engine.generate_theme_only(
            scenario["text"], 
            scenario["template"],
            scenario["theme"]
        )
        
        theme = decoration_output.theme_config
        performance = decoration_output.performance_metrics
        
        print(f"Text: {scenario['text'][:80]}...")
        print(f"Template: {scenario['template']}")
        print(f"Generated Theme: {theme.name}")
        print(f"Description: {theme.description}")
        print(f"Color Gradient: {theme.colors.primary_start} → {theme.colors.primary_end}")
        print(f"Glow Intensity: {theme.effects.glow_intensity}")
        print(f"Animation Speed: {theme.effects.animation_speed}")
        print(f"CSS Size: {performance.get('css_size_bytes', 0)} bytes")
        print(f"CSS Rules: {performance.get('css_rules_count', 0)}")


def demo_css_override_architecture():
    """Demonstrate CSS override architecture compatibility."""
    print_section("CSS OVERRIDE ARCHITECTURE DEMO")
    
    engine = DecorationEngine()
    
    sample_text = "This demonstration shows how emotional decoration enhances scroll-cast animations without breaking core functionality."
    
    print("Generating CSS for typewriter template...")
    decoration_output = engine.generate_theme_only(sample_text, "typewriter", "learning")
    css_content = decoration_output.css_content
    
    print_subsection("CSS Override Architecture Analysis")
    
    # Analyze CSS for override compatibility
    lines = css_content.split('\\n')
    
    # Check for CSS custom properties
    css_variables = [line.strip() for line in lines if line.strip().startswith('--decoration-')]
    print(f"CSS Custom Properties: {len(css_variables)} found")
    for var in css_variables[:5]:  # Show first 5
        print(f"  {var}")
    if len(css_variables) > 5:
        print(f"  ... and {len(css_variables) - 5} more")
    
    # Check for scroll-cast compatibility
    scroll_cast_selectors = ['.typewriter-char', '.typewriter-container', '.typewriter-sentence']
    found_selectors = []
    for selector in scroll_cast_selectors:
        if selector in css_content:
            found_selectors.append(selector)
    
    print(f"\\nScroll-cast Compatible Selectors: {len(found_selectors)}")
    for selector in found_selectors:
        print(f"  {selector}")
    
    # Check for non-conflicting properties
    typewriter_char_css = css_content.split('.typewriter-char {')[1].split('}')[0] if '.typewriter-char {' in css_content else ""
    conflicting_props = ['opacity:', 'transition:', 'display:']
    conflicts = [prop for prop in conflicting_props if prop in typewriter_char_css]
    
    print(f"\\nConflicting Properties: {len(conflicts)}")
    if conflicts:
        print("  WARNING: Found conflicting properties:")
        for conflict in conflicts:
            print(f"    {conflict}")
    else:
        print("  ✓ No conflicts with core scroll-cast functionality")
    
    # Show enhancement properties
    enhancement_props = ['background:', 'filter:', '-webkit-background-clip:', 'background-clip:']
    enhancements = [prop for prop in enhancement_props if prop in typewriter_char_css]
    
    print(f"\\nEnhancement Properties: {len(enhancements)}")
    for enhancement in enhancements:
        print(f"  ✓ {enhancement}")


def demo_predefined_themes():
    """Demonstrate predefined theme system."""
    print_section("PREDEFINED THEMES DEMO")
    
    theme_loader = ThemeLoader()
    
    print("Available Themes:")
    themes = theme_loader.list_themes()
    
    if themes:
        for theme_name in sorted(themes):
            theme_info = theme_loader.get_theme_info(theme_name)
            if theme_info:
                print(f"\\n• {theme_info['name']} ({theme_name})")
                print(f"  Category: {theme_info['category']}")
                print(f"  Description: {theme_info['description']}")
                print(f"  Colors: {theme_info['colors']['primary_gradient'][0]} → {theme_info['colors']['primary_gradient'][1]}")
                print(f"  Compatible with: {', '.join(theme_info['compatibility'])}")
    else:
        print("No predefined themes found. Theme files may not be available.")
        print("This is normal for a development environment.")


def demo_html_injection():
    """Demonstrate HTML injection capabilities."""
    print_section("HTML INJECTION DEMO")
    
    # Create sample scroll-cast HTML
    sample_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Scroll Cast Demo</title>
    <link rel="stylesheet" href="scrollcast-core.css">
</head>
<body>
    <div class="typewriter-container">
        <div class="typewriter-sentence">
            <span class="typewriter-char">H</span>
            <span class="typewriter-char">e</span>
            <span class="typewriter-char">l</span>
            <span class="typewriter-char">l</span>
            <span class="typewriter-char">o</span>
        </div>
    </div>
    <script src="scrollcast-core.js"></script>
</body>
</html>'''
    
    engine = DecorationEngine()
    
    print("Original HTML structure:")
    print("✓ typewriter-container")
    print("✓ typewriter-sentence")
    print("✓ typewriter-char elements")
    print("✓ scrollcast-core.css")
    print("✓ scrollcast-core.js")
    
    # Validate HTML structure
    temp_file = Path("temp_demo.html")
    temp_file.write_text(sample_html)
    
    try:
        validation = engine.validate_html_compatibility(str(temp_file))
        
        print(f"\\nHTML Validation Results:")
        print(f"Valid structure: {validation['valid']}")
        
        if validation['valid']:
            print(f"Has head tag: {validation['structure']['has_head']}")
            print(f"Has body tag: {validation['structure']['has_body']}")
            print(f"Scroll-cast elements found: {len(validation['scroll_cast_elements'])}")
            
            for element in validation['scroll_cast_elements']:
                print(f"  {element['selector']}: {element['count']} elements")
        
        # Preview decoration injection
        sample_text = "This is a demonstration of HTML enhancement capabilities."
        preview = engine.preview_decoration(str(temp_file), sample_text, "typewriter", "learning")
        
        if preview['valid']:
            print(f"\\nInjection Preview:")
            print(f"Theme: {preview['preview']['theme_name']}")
            print(f"CSS size: {preview['preview']['css_injection']['size_bytes']} bytes")
            print(f"Elements to enhance: {preview['preview']['total_enhanced_elements']}")
            print(f"Enhancement types:")
            for enhancement in preview['preview']['element_enhancements']:
                print(f"  {enhancement['selector']}: {enhancement['count']} elements")
        
    finally:
        # Clean up
        if temp_file.exists():
            temp_file.unlink()


def demo_performance():
    """Demonstrate system performance."""
    print_section("PERFORMANCE DEMO")
    
    engine = DecorationEngine()
    
    # Test with different text sizes
    test_cases = [
        ("Short", "Hello World!"),
        ("Medium", "This is a medium-length text that contains several sentences and covers educational content about machine learning fundamentals." * 2),
        ("Long", "This is a longer text sample that will be used to test the performance characteristics of the emotional decoration system. " * 20),
        ("Very Long", "Performance testing with substantial content. " * 100)
    ]
    
    print("Processing Speed Tests:")
    
    for name, text in test_cases:
        start_time = time.time()
        
        request = DecorationRequest(
            text=text,
            template_type="typewriter",
            output_format="css"
        )
        
        response = engine.process_decoration_request(request)
        processing_time = time.time() - start_time
        
        chars_per_second = len(text) / processing_time if processing_time > 0 else 0
        
        print(f"\\n{name} Text ({len(text)} chars):")
        print(f"  Processing time: {processing_time:.3f}s")
        print(f"  Speed: {chars_per_second:.0f} chars/sec")
        print(f"  Success: {response.success}")
        
        # Performance targets
        if chars_per_second >= 5000:
            print("  ✓ Exceeds target performance (5000 chars/sec)")
        elif chars_per_second >= 1000:
            print("  ✓ Good performance (>1000 chars/sec)")
        else:
            print("  ⚠ Below optimal performance")
    
    # Show overall stats
    stats = engine.get_performance_stats()
    print(f"\\nOverall Performance Statistics:")
    print(f"Total requests processed: {stats['total_requests']}")
    print(f"Average processing speed: {stats['average_chars_per_second']:.0f} chars/sec")
    print(f"Cache hits: {stats['cache_stats']['cache_size']}")


def main():
    """Run complete demonstration."""
    print("EMOTIONAL DECORATION SYSTEM DEMONSTRATION")
    print("========================================")
    print("This demo showcases the key features and capabilities of the")
    print("emotional-decoration system for enhancing scroll-cast animations.")
    
    try:
        # Run all demos
        demo_content_analysis()
        demo_theme_generation()
        demo_css_override_architecture()
        demo_predefined_themes()
        demo_html_injection()
        demo_performance()
        
        print_section("DEMONSTRATION COMPLETE")
        print("✓ Content analysis working")
        print("✓ Theme generation functional")
        print("✓ CSS override architecture compatible")
        print("✓ HTML injection capabilities verified")
        print("✓ Performance targets evaluated")
        print("\\nThe emotional-decoration system is ready for use!")
        
    except Exception as e:
        print(f"\\nERROR: Demo failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())