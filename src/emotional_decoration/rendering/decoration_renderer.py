"""Decoration rendering system for emotional-decoration."""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from ..models import ThemeConfig, DecorationOutput, DecorationRequest, DecorationResponse
from ..packing.css_generator import CSSGenerator


class DecorationRenderer:
    """Renders decoration files and manages output generation."""
    
    def __init__(self, output_dir: str = "decorations"):
        self.output_dir = Path(output_dir)
        self.css_generator = CSSGenerator()
        self.output_dir.mkdir(exist_ok=True)
        
    def render_decoration(
        self, 
        theme_config: ThemeConfig, 
        template_type: str = "typewriter",
        output_name: Optional[str] = None
    ) -> DecorationOutput:
        """
        Render complete decoration output.
        
        Args:
            theme_config: Theme configuration
            template_type: Target scroll-cast template type
            output_name: Optional custom output name
            
        Returns:
            DecorationOutput with generated content
        """
        # Generate CSS content
        css_content = self.css_generator.generate_css(theme_config, template_type)
        
        # Generate JavaScript content (optional)
        js_content = self._generate_javascript(theme_config, template_type)
        
        # Generate manifest
        manifest = self._generate_manifest(theme_config, template_type)
        
        # Calculate performance metrics
        performance_metrics = self._calculate_performance_metrics(css_content, js_content)
        
        return DecorationOutput(
            css_content=css_content,
            js_content=js_content,
            theme_config=theme_config,
            manifest=manifest,
            performance_metrics=performance_metrics
        )
    
    def save_decoration(
        self, 
        decoration_output: DecorationOutput, 
        name: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Save decoration output to files.
        
        Args:
            decoration_output: Decoration output to save
            name: Optional custom name for files
            
        Returns:
            Dictionary mapping file types to their paths
        """
        if not name:
            name = self._sanitize_filename(decoration_output.theme_config.name)
        
        file_paths = {}
        
        # Save CSS file
        css_path = self.output_dir / f"{name}.css"
        css_path.write_text(decoration_output.css_content, encoding='utf-8')
        file_paths['css'] = str(css_path)
        
        # Save minified CSS
        minified_css = self.css_generator.generate_minified_css(
            decoration_output.theme_config
        )
        css_min_path = self.output_dir / f"{name}.min.css"
        css_min_path.write_text(minified_css, encoding='utf-8')
        file_paths['css_min'] = str(css_min_path)
        
        # Save JavaScript if present
        if decoration_output.js_content:
            js_path = self.output_dir / f"{name}.js"
            js_path.write_text(decoration_output.js_content, encoding='utf-8')
            file_paths['js'] = str(js_path)
        
        # Save manifest
        manifest_path = self.output_dir / f"{name}.manifest.json"
        manifest_path.write_text(
            json.dumps(decoration_output.manifest, indent=2), 
            encoding='utf-8'
        )
        file_paths['manifest'] = str(manifest_path)
        
        # Save theme config
        config_path = self.output_dir / f"{name}.config.json"
        config_path.write_text(
            json.dumps(decoration_output.theme_config.dict(), indent=2),
            encoding='utf-8'
        )
        file_paths['config'] = str(config_path)
        
        return file_paths
    
    def load_decoration(self, name: str) -> Optional[DecorationOutput]:
        """
        Load decoration from saved files.
        
        Args:
            name: Name of the decoration to load
            
        Returns:
            DecorationOutput if found, None otherwise
        """
        config_path = self.output_dir / f"{name}.config.json"
        css_path = self.output_dir / f"{name}.css"
        manifest_path = self.output_dir / f"{name}.manifest.json"
        
        if not all(p.exists() for p in [config_path, css_path, manifest_path]):
            return None
        
        try:
            # Load theme config
            with open(config_path, 'r', encoding='utf-8') as f:
                theme_data = json.load(f)
                theme_config = ThemeConfig(**theme_data)
            
            # Load CSS content
            css_content = css_path.read_text(encoding='utf-8')
            
            # Load JavaScript content if it exists
            js_path = self.output_dir / f"{name}.js"
            js_content = js_path.read_text(encoding='utf-8') if js_path.exists() else None
            
            # Load manifest
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
            
            return DecorationOutput(
                css_content=css_content,
                js_content=js_content,
                theme_config=theme_config,
                manifest=manifest,
                performance_metrics={}
            )
            
        except Exception:
            return None
    
    def list_decorations(self) -> List[Dict[str, any]]:
        """
        List all available decorations.
        
        Returns:
            List of decoration metadata
        """
        decorations = []
        
        for config_file in self.output_dir.glob("*.config.json"):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    theme_data = json.load(f)
                
                name = config_file.stem.replace('.config', '')
                decorations.append({
                    'name': name,
                    'theme_name': theme_data.get('name', 'Unknown'),
                    'description': theme_data.get('description', 'No description'),
                    'compatibility': theme_data.get('compatibility', []),
                    'file_path': str(config_file)
                })
            except Exception:
                continue
        
        return decorations
    
    def delete_decoration(self, name: str) -> bool:
        """
        Delete a decoration and all its files.
        
        Args:
            name: Name of the decoration to delete
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            # List of file extensions to delete
            extensions = ['.css', '.min.css', '.js', '.manifest.json', '.config.json']
            
            deleted_count = 0
            for ext in extensions:
                file_path = self.output_dir / f"{name}{ext}"
                if file_path.exists():
                    file_path.unlink()
                    deleted_count += 1
            
            return deleted_count > 0
            
        except Exception:
            return False
    
    def _generate_javascript(self, theme_config: ThemeConfig, template_type: str) -> Optional[str]:
        """Generate optional JavaScript for interactive effects."""
        if not theme_config.effects.pulse_enabled:
            return None
        
        return f"""
/**
 * Emotional Decoration JavaScript
 * Theme: {theme_config.name}
 * Compatible with: {template_type}
 */

(function() {{
    'use strict';
    
    // Decoration enhancement functionality
    class DecorationEnhancer {{
        constructor() {{
            this.initialized = false;
            this.observers = [];
        }}
        
        init() {{
            if (this.initialized) return;
            
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', () => this.enhance());
            }} else {{
                this.enhance();
            }}
            
            this.initialized = true;
        }}
        
        enhance() {{
            // Find elements to enhance
            const elements = this.findTargetElements();
            
            // Apply enhancements
            elements.forEach(element => this.enhanceElement(element));
            
            // Set up intersection observer for performance
            this.setupIntersectionObserver(elements);
            
            // Set up resize observer for responsive behavior
            this.setupResizeObserver();
        }}
        
        findTargetElements() {{
            const selectors = [
                '.typewriter-char',
                '.railway-line', 
                '.scroll-line'
            ];
            
            return Array.from(document.querySelectorAll(selectors.join(', ')));
        }}
        
        enhanceElement(element) {{
            // Add decoration enhancement class
            element.classList.add('decoration-enhanced');
            
            // Add pulse class if enabled
            if ({str(theme_config.effects.pulse_enabled).lower()}) {{
                element.classList.add('pulse-enabled');
            }}
            
            // Add hover effects
            this.addHoverEffects(element);
        }}
        
        addHoverEffects(element) {{
            element.addEventListener('mouseenter', () => {{
                element.style.setProperty('--decoration-glow-intensity', '{theme_config.effects.glow_intensity * 1.2}');
            }});
            
            element.addEventListener('mouseleave', () => {{
                element.style.setProperty('--decoration-glow-intensity', '{theme_config.effects.glow_intensity}');
            }});
        }}
        
        setupIntersectionObserver(elements) {{
            if (!window.IntersectionObserver) return;
            
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.classList.add('in-view');
                    }} else {{
                        entry.target.classList.remove('in-view');
                    }}
                }});
            }}, {{
                threshold: 0.1,
                rootMargin: '50px'
            }});
            
            elements.forEach(element => observer.observe(element));
            this.observers.push(observer);
        }}
        
        setupResizeObserver() {{
            if (!window.ResizeObserver) return;
            
            const observer = new ResizeObserver(() => {{
                // Recalculate responsive variables
                this.updateResponsiveVariables();
            }});
            
            observer.observe(document.body);
            this.observers.push(observer);
        }}
        
        updateResponsiveVariables() {{
            const width = window.innerWidth;
            let scaleFactor = 1;
            
            if (width <= 480) {{
                scaleFactor = 0.6;
            }} else if (width <= 768) {{
                scaleFactor = 0.8;
            }} else if (width >= 1200) {{
                scaleFactor = 1.2;
            }}
            
            document.documentElement.style.setProperty(
                '--decoration-responsive-scale',
                scaleFactor.toString()
            );
        }}
        
        destroy() {{
            // Clean up observers
            this.observers.forEach(observer => observer.disconnect());
            this.observers = [];
            
            // Remove enhancement classes
            const elements = document.querySelectorAll('.decoration-enhanced');
            elements.forEach(element => {{
                element.classList.remove('decoration-enhanced', 'pulse-enabled', 'in-view');
            }});
            
            this.initialized = false;
        }}
    }}
    
    // Initialize enhancement system
    const enhancer = new DecorationEnhancer();
    enhancer.init();
    
    // Export for external use
    window.EmotionalDecoration = {{
        enhancer: enhancer,
        version: '1.0.0',
        theme: '{theme_config.name}'
    }};
    
    // Performance monitoring
    if (window.performance && window.performance.mark) {{
        window.performance.mark('emotional-decoration-loaded');
    }}
}})();
"""
    
    def _generate_manifest(self, theme_config: ThemeConfig, template_type: str) -> Dict[str, any]:
        """Generate decoration manifest with metadata."""
        return {
            "version": "1.0.0",
            "name": theme_config.name,
            "description": theme_config.description,
            "author": "emotional-decoration",
            "license": "MIT",
            "compatibility": {
                "scroll_cast_templates": theme_config.compatibility,
                "target_template": template_type
            },
            "features": {
                "css_variables": True,
                "responsive_design": True,
                "accessibility": True,
                "pulse_animation": theme_config.effects.pulse_enabled,
                "glow_effects": theme_config.effects.glow_intensity > 0,
                "blur_effects": theme_config.effects.blur_radius > 0
            },
            "performance": {
                "hardware_acceleration": True,
                "reduced_motion_support": True,
                "mobile_optimized": True
            },
            "colors": {
                "primary_gradient": [
                    theme_config.colors.primary_start,
                    theme_config.colors.primary_end
                ],
                "background_gradient": [
                    theme_config.colors.background_start,
                    theme_config.colors.background_end
                ],
                "accent": theme_config.colors.accent_color,
                "glow": theme_config.colors.glow_color
            },
            "effects": {
                "glow_intensity": theme_config.effects.glow_intensity,
                "animation_speed": theme_config.effects.animation_speed,
                "blur_radius": theme_config.effects.blur_radius,
                "gradient_angle": theme_config.effects.gradient_angle
            }
        }
    
    def _calculate_performance_metrics(self, css_content: str, js_content: Optional[str]) -> Dict[str, float]:
        """Calculate performance metrics for the decoration."""
        css_size = len(css_content.encode('utf-8'))
        js_size = len(js_content.encode('utf-8')) if js_content else 0
        
        # Estimate compression ratios
        css_gzip_estimate = css_size * 0.3  # Rough gzip estimate
        js_gzip_estimate = js_size * 0.4 if js_content else 0
        
        return {
            "css_size_bytes": css_size,
            "js_size_bytes": js_size,
            "total_size_bytes": css_size + js_size,
            "estimated_gzip_size": css_gzip_estimate + js_gzip_estimate,
            "css_rules_count": css_content.count('{'),
            "css_variables_count": css_content.count('--decoration-'),
            "compression_ratio": (css_gzip_estimate + js_gzip_estimate) / max(css_size + js_size, 1)
        }
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename by removing invalid characters."""
        import re
        # Remove invalid characters and replace with underscores
        sanitized = re.sub(r'[^\w\-_\.]', '_', name)
        # Remove multiple consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        return sanitized or 'decoration'