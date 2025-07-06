#!/usr/bin/env python3
"""
Simple test to verify basic functionality without external dependencies.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_models():
    """Test basic model functionality."""
    print("Testing models...")
    
    try:
        from emotional_decoration.models import (
            ColorScheme, VisualEffect, ThemeConfig,
            EmotionType, ContentType, DifficultyLevel
        )
        
        # Test ColorScheme
        colors = ColorScheme(
            primary_start="#4A90E2",
            primary_end="#7ED321",
            background_start="#000428",
            background_end="#004e92",
            accent_color="#50E3C2",
            glow_color="#4A90E2"
        )
        print(f"✅ ColorScheme created: {colors.primary_start} → {colors.primary_end}")
        
        # Test VisualEffect
        effects = VisualEffect(
            glow_intensity=0.5,
            animation_speed=1.0
        )
        print(f"✅ VisualEffect created: glow={effects.glow_intensity}, speed={effects.animation_speed}")
        
        # Test ThemeConfig
        theme = ThemeConfig(
            name="Test Theme",
            description="A test theme",
            colors=colors,
            effects=effects,
            typography={"font_weight": "normal"},
            compatibility=["typewriter"]
        )
        print(f"✅ ThemeConfig created: {theme.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False


def test_css_generation():
    """Test CSS generation without external dependencies."""
    print("\\nTesting CSS generation...")
    
    try:
        from emotional_decoration.packing.css_generator import CSSGenerator
        from emotional_decoration.models import ColorScheme, VisualEffect, ThemeConfig
        
        # Create test theme
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
            pulse_enabled=True
        )
        
        theme = ThemeConfig(
            name="Test Theme",
            description="A test theme for CSS generation",
            colors=colors,
            effects=effects,
            typography={"font_weight": "normal"},
            compatibility=["typewriter"]
        )
        
        # Generate CSS
        generator = CSSGenerator()
        css = generator.generate_css(theme, "typewriter")
        
        print(f"✅ CSS generated: {len(css)} characters")
        
        # Check for key elements
        checks = [
            ("CSS variables", "--decoration-primary-start" in css),
            ("Typewriter selector", ".typewriter-char" in css),
            ("Linear gradient", "linear-gradient" in css),
            ("Background clip", "background-clip" in css),
            ("CSS custom properties", ":root {" in css)
        ]
        
        all_passed = True
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"  {status} {check_name}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ CSS generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scroll_cast_compatibility():
    """Test compatibility with scroll-cast HTML structure."""
    print("\\nTesting scroll-cast compatibility...")
    
    # Sample scroll-cast HTML structure
    sample_html = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ScrollCast Demo</title>
    <link rel="stylesheet" href="shared/scrollcast-styles.css">
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
</body>
</html>'''
    
    try:
        from emotional_decoration.rendering.html_injector import HTMLInjector
        
        # Save sample HTML
        html_file = Path("test_sample.html")
        html_file.write_text(sample_html, encoding='utf-8')
        
        # Test HTML validation
        injector = HTMLInjector()
        validation = injector.validate_html_structure(str(html_file))
        
        print(f"✅ HTML validation: {validation['valid']}")
        
        if validation['valid']:
            print(f"  Structure check: head={validation['structure']['has_head']}, body={validation['structure']['has_body']}")
            print(f"  Scroll-cast elements: {len(validation['scroll_cast_elements'])}")
            
            for element in validation['scroll_cast_elements']:
                print(f"    {element['selector']}: {element['count']} elements")
        
        # Clean up
        if html_file.exists():
            html_file.unlink()
        
        return validation['valid']
        
    except Exception as e:
        print(f"❌ Compatibility test failed: {e}")
        # Clean up on error
        html_file = Path("test_sample.html")
        if html_file.exists():
            html_file.unlink()
        return False


def test_theme_loading():
    """Test theme loading functionality."""
    print("\\nTesting theme loading...")
    
    try:
        from emotional_decoration.themes.theme_loader import ThemeLoader
        
        loader = ThemeLoader()
        themes = loader.list_themes()
        
        print(f"✅ ThemeLoader created")
        print(f"  Available themes: {len(themes)}")
        
        if themes:
            for theme_name in themes[:3]:  # Show first 3
                theme_info = loader.get_theme_info(theme_name)
                if theme_info:
                    print(f"    • {theme_info['name']} ({theme_name})")
        else:
            print("    (No predefined themes found - this is normal for development)")
        
        return True
        
    except Exception as e:
        print(f"❌ Theme loading test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("EMOTIONAL-DECORATION BASIC FUNCTIONALITY TEST")
    print("==============================================")
    
    tests = [
        ("Models", test_models),
        ("CSS Generation", test_css_generation),
        ("Scroll-cast Compatibility", test_scroll_cast_compatibility),
        ("Theme Loading", test_theme_loading),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\\n{'='*50}")
        print(f"Running {test_name} Test")
        print(f"{'='*50}")
        
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\\n🎉 All tests passed! The emotional-decoration system is working correctly.")
        print("\\nNext steps:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run integration_demo.py with real scroll-cast files")
        print("3. Test CLI commands: emotional-decoration --help")
    else:
        print(f"\\n⚠️  {total - passed} tests failed. Please check the implementation.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)