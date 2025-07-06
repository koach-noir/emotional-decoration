#!/usr/bin/env python3
"""
Direct CSS generation without problematic imports.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import only the specific modules we need
from emotional_decoration.models import ColorScheme, VisualEffect, ThemeConfig
from emotional_decoration.packing.css_generator import CSSGenerator

def generate_samples():
    """Generate CSS samples directly."""
    print("Generating CSS samples with direct imports...")
    
    # Create output directory
    output_dir = Path("css_output")
    output_dir.mkdir(exist_ok=True)
    
    # Define themes
    themes = {
        "learning_focused": {
            "name": "Learning Focused",
            "description": "Blue-green gradient optimized for educational content",
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
            "description": "Clean sophisticated theme for business content",
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
            "description": "Dynamic warm theme for expressive content",
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
    total_size = 0
    
    for theme_name, theme_data in themes.items():
        print(f"\\n📋 Generating {theme_name.replace('_', ' ').title()} theme...")
        
        # Create theme config
        theme_config = ThemeConfig(
            name=theme_data["name"],
            description=theme_data["description"],
            colors=theme_data["colors"],
            effects=theme_data["effects"],
            typography={
                "font_weight": "500",
                "letter_spacing": "0.01em",
                "line_height": "1.6"
            },
            compatibility=templates
        )
        
        for template in templates:
            # Generate CSS
            css_content = generator.generate_css(theme_config, template)
            
            # Save normal version
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
            total_size += css_size + min_size
            css_rules = css_content.count('{')
            css_vars = css_content.count('--decoration-')
            
            print(f"   ✅ {template:10} | {css_size:5,} chars | {min_size:4,} min | {css_rules:2d} rules | {css_vars:2d} vars")
            
            generated_files.extend([css_filepath, min_filepath])
    
    # Create integration guide
    guide_content = f"""# Emotional Decoration CSS Files

Generated {len(generated_files)} CSS files for scroll-cast integration.

## Usage

### Step 1: Include CSS after scroll-cast styles

```html
<!DOCTYPE html>
<html>
<head>
    <!-- Original scroll-cast styles -->
    <link rel="stylesheet" href="shared/scrollcast-styles.css">
    
    <!-- Add emotional decoration enhancement -->
    <link rel="stylesheet" href="learning_focused_typewriter.css">
</head>
<body>
    <!-- Your scroll-cast HTML structure -->
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
</html>
```

### Step 2: (Optional) Add enhancement classes

For maximum effect, add `decoration-enhanced` class to elements:

```html
<span class="typewriter-char decoration-enhanced">H</span>
```

## Available Themes

### Learning Themes
- `learning_focused_typewriter.css` - Focused blue-green gradient
- `learning_focused_railway.css` - Railway version
- `learning_focused_scroll.css` - Scroll version

### Professional Themes  
- `professional_minimal_typewriter.css` - Clean minimal style
- `professional_minimal_railway.css` - Railway version
- `professional_minimal_scroll.css` - Scroll version

### Emotional Themes
- `emotional_vibrant_typewriter.css` - Vibrant warm colors
- `emotional_vibrant_railway.css` - Railway version
- `emotional_vibrant_scroll.css` - Scroll version

## Customization

Each CSS file includes CSS custom properties for easy customization:

```css
:root {{
    --decoration-primary-start: #4A90E2;
    --decoration-primary-end: #7ED321;
    --decoration-glow-intensity: 0.3;
    /* ... more variables */
}}
```

You can override these in your own CSS to customize colors and effects.

## Technical Details

- **Total files**: {len(generated_files)}
- **Total size**: {total_size:,} bytes
- **Architecture**: CSS Override compatible with scroll-cast
- **Responsive**: Mobile-friendly design included
- **Accessibility**: Reduced motion support included

Generated by emotional-decoration v1.0.0
"""
    
    guide_path = output_dir / "README.md"
    guide_path.write_text(guide_content, encoding='utf-8')
    
    # Create a demo HTML file
    demo_html = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Emotional Decoration Demo</title>
    
    <!-- Base scroll-cast styles simulation -->
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background: #000;
            color: #fff;
            height: 100vh;
            overflow: hidden;
        }
        
        .typewriter-container {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            width: 90%;
            max-width: 600px;
            line-height: 1.4;
        }
        
        .typewriter-char {
            opacity: 1;
            transition: opacity 0.2s ease-in-out;
            display: inline-block;
        }
    </style>
    
    <!-- Emotional decoration enhancement -->
    <link rel="stylesheet" href="learning_focused_typewriter.css">
</head>
<body>
    <div class="typewriter-container">
        <div class="typewriter-sentence">
            <span class="typewriter-char decoration-enhanced">W</span>
            <span class="typewriter-char decoration-enhanced">e</span>
            <span class="typewriter-char decoration-enhanced">l</span>
            <span class="typewriter-char decoration-enhanced">c</span>
            <span class="typewriter-char decoration-enhanced">o</span>
            <span class="typewriter-char decoration-enhanced">m</span>
            <span class="typewriter-char decoration-enhanced">e</span>
            <span class="typewriter-char decoration-enhanced"> </span>
            <span class="typewriter-char decoration-enhanced">t</span>
            <span class="typewriter-char decoration-enhanced">o</span>
            <span class="typewriter-char decoration-enhanced"> </span>
            <span class="typewriter-char decoration-enhanced">E</span>
            <span class="typewriter-char decoration-enhanced">m</span>
            <span class="typewriter-char decoration-enhanced">o</span>
            <span class="typewriter-char decoration-enhanced">t</span>
            <span class="typewriter-char decoration-enhanced">i</span>
            <span class="typewriter-char decoration-enhanced">o</span>
            <span class="typewriter-char decoration-enhanced">n</span>
            <span class="typewriter-char decoration-enhanced">a</span>
            <span class="typewriter-char decoration-enhanced">l</span>
            <span class="typewriter-char decoration-enhanced"> </span>
            <span class="typewriter-char decoration-enhanced">D</span>
            <span class="typewriter-char decoration-enhanced">e</span>
            <span class="typewriter-char decoration-enhanced">c</span>
            <span class="typewriter-char decoration-enhanced">o</span>
            <span class="typewriter-char decoration-enhanced">r</span>
            <span class="typewriter-char decoration-enhanced">a</span>
            <span class="typewriter-char decoration-enhanced">t</span>
            <span class="typewriter-char decoration-enhanced">i</span>
            <span class="typewriter-char decoration-enhanced">o</span>
            <span class="typewriter-char decoration-enhanced">n</span>
        </div>
    </div>
</body>
</html>'''
    
    demo_path = output_dir / "demo.html"
    demo_path.write_text(demo_html, encoding='utf-8')
    
    print(f"\\n🎉 Generation Complete!")
    print(f"   📁 Output directory: {output_dir}")
    print(f"   📄 Files generated: {len(generated_files)}")
    print(f"   📊 Total size: {total_size:,} bytes")
    print(f"   📋 Usage guide: {guide_path}")
    print(f"   🌐 Demo file: {demo_path}")
    
    return output_dir, generated_files

if __name__ == "__main__":
    try:
        output_dir, files = generate_samples()
        print(f"\\n✨ Ready to use! Open {output_dir}/demo.html in a browser to see the effects.")
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)