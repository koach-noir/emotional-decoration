#!/usr/bin/env python3
"""
Manual test to generate CSS samples and verify output.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def generate_css_samples_manually():
    """Generate CSS samples using only working components."""
    print("Generating CSS samples manually...")
    
    try:
        # Import only the CSS generator (which we know works)
        from emotional_decoration.packing.css_generator import CSSGenerator
        from emotional_decoration.models import ColorScheme, VisualEffect, ThemeConfig
        
        # Create output directory
        output_dir = Path("generated_css_samples")
        output_dir.mkdir(exist_ok=True)
        
        # Define themes manually (since we know the YAML loading works)
        themes = {
            "learning_focused": {
                "name": "Learning Focused",
                "description": "Blue-green gradient theme optimized for educational content",
                "colors": ColorScheme(
                    primary_start="#4A90E2",
                    primary_end="#7ED321",
                    background_start="#000428",
                    background_end="#004e92",
                    accent_color="#50E3C2",
                    glow_color="#4A90E2"
                ),
                "effects": VisualEffect(
                    glow_intensity=0.3,
                    animation_speed=0.8,
                    pulse_enabled=False,
                    gradient_angle=45
                )
            },
            "professional_minimal": {
                "name": "Professional Minimal",
                "description": "Clean gray-blue theme for business content",
                "colors": ColorScheme(
                    primary_start="#2F3542",
                    primary_end="#57606F",
                    background_start="#F8F9FA",
                    background_end="#E9ECEF",
                    accent_color="#3742FA",
                    glow_color="#2F3542"
                ),
                "effects": VisualEffect(
                    glow_intensity=0.2,
                    animation_speed=0.7,
                    pulse_enabled=False,
                    gradient_angle=0
                )
            },
            "emotional_vibrant": {
                "name": "Emotional Vibrant",
                "description": "Dynamic coral-gold theme for expressive emotional content",
                "colors": ColorScheme(
                    primary_start="#FF7675",
                    primary_end="#FDCB6E",
                    background_start="#6C5CE7",
                    background_end="#A29BFE",
                    accent_color="#FD79A8",
                    glow_color="#FF7675"
                ),
                "effects": VisualEffect(
                    glow_intensity=0.6,
                    animation_speed=1.2,
                    pulse_enabled=True,
                    gradient_angle=135
                )
            }
        }
        
        # Create CSS generator
        generator = CSSGenerator()
        templates = ["typewriter", "railway", "scroll"]
        
        generated_files = []
        
        for theme_name, theme_data in themes.items():
            print(f"\\nGenerating {theme_name} theme...")
            
            # Create theme config
            theme_config = ThemeConfig(
                name=theme_data["name"],
                description=theme_data["description"],
                colors=theme_data["colors"],
                effects=theme_data["effects"],
                typography={"font_weight": "normal", "letter_spacing": "0.01em"},
                compatibility=templates
            )
            
            for template in templates:
                try:
                    # Generate CSS
                    css_content = generator.generate_css(theme_config, template)
                    
                    # Save to file
                    css_filename = f"{theme_name}_{template}.css"
                    css_filepath = output_dir / css_filename
                    css_filepath.write_text(css_content, encoding='utf-8')
                    
                    # Generate minified version
                    minified_css = generator.generate_minified_css(theme_config, template)
                    min_filename = f"{theme_name}_{template}.min.css"
                    min_filepath = output_dir / min_filename
                    min_filepath.write_text(minified_css, encoding='utf-8')
                    
                    # Stats
                    css_size = len(css_content)
                    min_size = len(minified_css)
                    css_rules = css_content.count('{')
                    css_vars = css_content.count('--decoration-')
                    
                    print(f"  ✅ {template:12} | {css_size:5d} chars | {min_size:5d} min | {css_rules:2d} rules | {css_vars:2d} vars")
                    
                    generated_files.extend([css_filepath, min_filepath])
                    
                except Exception as e:
                    print(f"  ❌ {template:12} | Error: {e}")
        
        # Generate index file
        index_content = f"""# Generated CSS Samples for Emotional Decoration

Generated {len(generated_files)} CSS files for scroll-cast integration.

## Theme Files

"""
        
        for theme_name in themes.keys():
            index_content += f"### {theme_name.replace('_', ' ').title()}\n"
            for template in templates:
                normal_file = f"{theme_name}_{template}.css"
                min_file = f"{theme_name}_{template}.min.css"
                if (output_dir / normal_file).exists():
                    index_content += f"- `{normal_file}` - Normal version\\n"
                    index_content += f"- `{min_file}` - Minified version\\n"
            index_content += "\\n"
        
        index_content += """## Usage

Include these CSS files after your scroll-cast CSS:

```html
<!-- scroll-cast base styles -->
<link rel="stylesheet" href="scrollcast-styles.css">

<!-- emotional decoration enhancement -->
<link rel="stylesheet" href="learning_focused_typewriter.css">
```

The decoration CSS will enhance your scroll-cast animations with:
- Color gradients
- Glow effects
- Enhanced typography
- Responsive design
- CSS custom properties for customization
"""
        
        (output_dir / "README.md").write_text(index_content, encoding='utf-8')
        
        print(f"\\n🎉 Generated {len(generated_files)} CSS files in: {output_dir}")
        return output_dir, generated_files
        
    except Exception as e:
        print(f"❌ Manual CSS generation failed: {e}")
        import traceback
        traceback.print_exc()
        return None, []


def test_with_real_scroll_cast_structure():
    """Test CSS with a real scroll-cast HTML structure."""
    print("\\nTesting with real scroll-cast HTML structure...")
    
    # Real structure from the files we saw earlier
    sample_html = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScrollCast - TypeWriter Effect (Plugin)</title>
    <!-- ScrollCast Shared Styles -->
    <link rel="stylesheet" href="shared/scrollcast-styles.css">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #000;
            color: #fff;
            height: 100vh;
            overflow: hidden;
            user-select: none;
            cursor: pointer;
        }
        
        .typewriter-container {
            font-size: 3.7vw;
            font-family: Arial, sans-serif;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-weight: bold;
            text-align: center;
            width: 90%;
            max-width: 400px;
            line-height: 1.4;
        }
        
        @media (min-width: 768px) {
            .typewriter-container {
                font-size: 40px;
                max-width: 600px;
            }
        }
    </style>
</head>
<body>
    <div class="typewriter-container">
        <div class="typewriter-sentence" data-sentence="0">
            <span class="typewriter-char" data-char-index="0" id="char-0">T</span>
            <span class="typewriter-char" data-char-index="1" id="char-1">o</span>
            <span class="typewriter-char" data-char-index="2" id="char-2">d</span>
            <span class="typewriter-char" data-char-index="3" id="char-3">a</span>
            <span class="typewriter-char" data-char-index="4" id="char-4">y</span>
            <span class="typewriter-char" data-char-index="5" id="char-5"> </span>
            <span class="typewriter-char" data-char-index="6" id="char-6">i</span>
            <span class="typewriter-char" data-char-index="7" id="char-7">s</span>
            <span class="typewriter-char" data-char-index="8" id="char-8"> </span>
            <span class="typewriter-char" data-char-index="9" id="char-9">a</span>
            <span class="typewriter-char" data-char-index="10" id="char-10"> </span>
            <span class="typewriter-char" data-char-index="11" id="char-11">b</span>
            <span class="typewriter-char" data-char-index="12" id="char-12">e</span>
            <span class="typewriter-char" data-char-index="13" id="char-13">a</span>
            <span class="typewriter-char" data-char-index="14" id="char-14">u</span>
            <span class="typewriter-char" data-char-index="15" id="char-15">t</span>
            <span class="typewriter-char" data-char-index="16" id="char-16">i</span>
            <span class="typewriter-char" data-char-index="17" id="char-17">f</span>
            <span class="typewriter-char" data-char-index="18" id="char-18">u</span>
            <span class="typewriter-char" data-char-index="19" id="char-19">l</span>
            <span class="typewriter-char" data-char-index="20" id="char-20"> </span>
            <span class="typewriter-char" data-char-index="21" id="char-21">d</span>
            <span class="typewriter-char" data-char-index="22" id="char-22">a</span>
            <span class="typewriter-char" data-char-index="23" id="char-23">y</span>
            <span class="typewriter-char" data-char-index="24" id="char-24">.</span>
        </div>
    </div>
    <script src="shared/scrollcast-core.js"></script>
</body>
</html>'''
    
    # Save as sample
    output_dir = Path("generated_css_samples")
    output_dir.mkdir(exist_ok=True)
    
    sample_file = output_dir / "scroll_cast_sample.html"
    sample_file.write_text(sample_html, encoding='utf-8')
    
    # Create enhanced version with decoration
    enhanced_html = sample_html.replace(
        '</head>',
        '''    <!-- Emotional Decoration Enhancement -->
    <link rel="stylesheet" href="learning_focused_typewriter.css">
</head>'''
    )
    
    # Add decoration classes to chars
    enhanced_html = enhanced_html.replace(
        'class="typewriter-char"',
        'class="typewriter-char decoration-enhanced"'
    )
    
    enhanced_file = output_dir / "scroll_cast_enhanced_sample.html"
    enhanced_file.write_text(enhanced_html, encoding='utf-8')
    
    print(f"✅ Created sample files:")
    print(f"   Original: {sample_file}")
    print(f"   Enhanced: {enhanced_file}")
    
    return [sample_file, enhanced_file]


def main():
    """Generate actual CSS samples and demo files."""
    print("EMOTIONAL-DECORATION MANUAL GENERATION TEST")
    print("===========================================")
    
    # Generate CSS samples
    css_dir, css_files = generate_css_samples_manually()
    
    if css_dir:
        print(f"\\n📁 CSS files location: {css_dir}")
        print("   Available CSS files:")
        for file in sorted(css_files):
            size = file.stat().st_size
            print(f"   • {file.name} ({size:,} bytes)")
    
    # Create demo HTML files
    demo_files = test_with_real_scroll_cast_structure()
    
    if demo_files:
        print(f"\\n📄 Demo HTML files:")
        for file in demo_files:
            print(f"   • {file}")
    
    print(f"\\n🎉 Generation complete!")
    print(f"\\nNext steps:")
    print(f"1. Open {css_dir}/README.md for usage instructions")
    print(f"2. View demo files in a browser to see the effects")
    print(f"3. Copy CSS files to your scroll-cast project")
    print(f"4. Include decoration CSS after scroll-cast styles")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)