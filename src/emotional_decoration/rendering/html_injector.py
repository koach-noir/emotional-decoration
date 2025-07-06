"""HTML injection system for adding decorations to existing scroll-cast HTML files."""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
from ..models import DecorationOutput


class HTMLInjector:
    """Injects decoration CSS/JS into existing HTML files."""
    
    def __init__(self):
        self.injection_markers = {
            'css_start': '<!-- EMOTIONAL-DECORATION-CSS-START -->',
            'css_end': '<!-- EMOTIONAL-DECORATION-CSS-END -->',
            'js_start': '<!-- EMOTIONAL-DECORATION-JS-START -->',
            'js_end': '<!-- EMOTIONAL-DECORATION-JS-END -->'
        }
    
    def inject_decoration(
        self, 
        html_file: str, 
        decoration_output: DecorationOutput,
        output_file: Optional[str] = None,
        inline_styles: bool = True
    ) -> str:
        """
        Inject decoration into HTML file.
        
        Args:
            html_file: Path to the source HTML file
            decoration_output: Decoration to inject
            output_file: Optional output file path
            inline_styles: Whether to inline CSS or link to external file
            
        Returns:
            Path to the enhanced HTML file
        """
        # Read source HTML
        html_path = Path(html_file)
        if not html_path.exists():
            raise FileNotFoundError(f"HTML file not found: {html_file}")
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Inject decoration
        self._inject_css(soup, decoration_output, inline_styles)
        self._inject_javascript(soup, decoration_output)
        self._add_decoration_classes(soup)
        self._add_meta_tags(soup, decoration_output)
        
        # Generate output content
        enhanced_html = str(soup)
        
        # Determine output path
        if not output_file:
            output_file = self._generate_output_filename(html_path, decoration_output)
        
        # Write enhanced HTML
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(enhanced_html)
        
        return str(output_path)
    
    def remove_decoration(self, html_file: str, output_file: Optional[str] = None) -> str:
        """
        Remove decoration from HTML file.
        
        Args:
            html_file: Path to the decorated HTML file
            output_file: Optional output file path
            
        Returns:
            Path to the cleaned HTML file
        """
        html_path = Path(html_file)
        if not html_path.exists():
            raise FileNotFoundError(f"HTML file not found: {html_file}")
        
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Remove decoration markers and content
        cleaned_html = self._remove_decoration_markers(html_content)
        
        # Parse and clean HTML
        soup = BeautifulSoup(cleaned_html, 'html.parser')
        self._remove_decoration_classes(soup)
        self._remove_decoration_meta_tags(soup)
        
        # Generate output content
        cleaned_html = str(soup)
        
        # Determine output path
        if not output_file:
            output_file = html_file.replace('.html', '_clean.html')
        
        # Write cleaned HTML
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_html)
        
        return str(output_path)
    
    def _inject_css(self, soup: BeautifulSoup, decoration_output: DecorationOutput, inline: bool = True):
        """Inject CSS into HTML head."""
        head = soup.find('head')
        if not head:
            # Create head if it doesn't exist
            head = soup.new_tag('head')
            if soup.html:
                soup.html.insert(0, head)
            else:
                soup.insert(0, head)
        
        # Remove existing decoration CSS
        self._remove_existing_decoration_css(head)
        
        if inline:
            # Inline CSS
            style_tag = soup.new_tag('style')
            style_tag.string = f"\\n{decoration_output.css_content}\\n"
            style_tag['data-decoration'] = 'emotional-decoration'
            
            # Add markers
            start_comment = soup.new_string(self.injection_markers['css_start'], 'comment')
            end_comment = soup.new_string(self.injection_markers['css_end'], 'comment')
            
            head.append(start_comment)
            head.append(style_tag)
            head.append(end_comment)
        else:
            # External CSS link
            link_tag = soup.new_tag('link')
            link_tag['rel'] = 'stylesheet'
            link_tag['href'] = f"{decoration_output.theme_config.name}.css"
            link_tag['data-decoration'] = 'emotional-decoration'
            
            start_comment = soup.new_string(self.injection_markers['css_start'], 'comment')
            end_comment = soup.new_string(self.injection_markers['css_end'], 'comment')
            
            head.append(start_comment)
            head.append(link_tag)
            head.append(end_comment)
    
    def _inject_javascript(self, soup: BeautifulSoup, decoration_output: DecorationOutput):
        """Inject JavaScript into HTML."""
        if not decoration_output.js_content:
            return
        
        # Remove existing decoration JS
        self._remove_existing_decoration_js(soup)
        
        # Create script tag
        script_tag = soup.new_tag('script')
        script_tag.string = f"\\n{decoration_output.js_content}\\n"
        script_tag['data-decoration'] = 'emotional-decoration'
        
        # Add markers
        start_comment = soup.new_string(self.injection_markers['js_start'], 'comment')
        end_comment = soup.new_string(self.injection_markers['js_end'], 'comment')
        
        # Insert before closing body tag or at end
        body = soup.find('body')
        if body:
            body.append(start_comment)
            body.append(script_tag)
            body.append(end_comment)
        else:
            soup.append(start_comment)
            soup.append(script_tag)
            soup.append(end_comment)
    
    def _add_decoration_classes(self, soup: BeautifulSoup):
        """Add decoration enhancement classes to relevant elements."""
        # Target elements based on scroll-cast naming conventions
        selectors_to_enhance = [
            '.typewriter-char',
            '.typewriter-container',
            '.typewriter-sentence',
            '.railway-line',
            '.railway-container',
            '.scroll-line',
            '.scroll-container'
        ]
        
        for selector in selectors_to_enhance:
            class_name = selector[1:]  # Remove the dot
            elements = soup.find_all(class_=class_name)
            
            for element in elements:
                # Add decoration enhancement class
                current_classes = element.get('class', [])
                if 'decoration-enhanced' not in current_classes:
                    current_classes.append('decoration-enhanced')
                    element['class'] = current_classes
    
    def _add_meta_tags(self, soup: BeautifulSoup, decoration_output: DecorationOutput):
        """Add meta tags with decoration information."""
        head = soup.find('head')
        if not head:
            return
        
        # Add decoration meta tags
        meta_tags = [
            ('decoration-theme', decoration_output.theme_config.name),
            ('decoration-version', '1.0.0'),
            ('decoration-compatibility', ','.join(decoration_output.theme_config.compatibility))
        ]
        
        for name, content in meta_tags:
            meta_tag = soup.new_tag('meta')
            meta_tag['name'] = name
            meta_tag['content'] = content
            head.append(meta_tag)
    
    def _remove_existing_decoration_css(self, head: BeautifulSoup):
        """Remove existing decoration CSS from head."""
        # Remove style tags with decoration marker
        for style in head.find_all('style', {'data-decoration': 'emotional-decoration'}):
            style.decompose()
        
        # Remove link tags with decoration marker
        for link in head.find_all('link', {'data-decoration': 'emotional-decoration'}):
            link.decompose()
    
    def _remove_existing_decoration_js(self, soup: BeautifulSoup):
        """Remove existing decoration JavaScript."""
        for script in soup.find_all('script', {'data-decoration': 'emotional-decoration'}):
            script.decompose()
    
    def _remove_decoration_markers(self, html_content: str) -> str:
        """Remove decoration markers and their content from HTML."""
        patterns = [
            (
                self.injection_markers['css_start'],
                self.injection_markers['css_end']
            ),
            (
                self.injection_markers['js_start'],
                self.injection_markers['js_end']
            )
        ]
        
        for start_marker, end_marker in patterns:
            pattern = f"{re.escape(start_marker)}.*?{re.escape(end_marker)}"
            html_content = re.sub(pattern, '', html_content, flags=re.DOTALL)
        
        return html_content
    
    def _remove_decoration_classes(self, soup: BeautifulSoup):
        """Remove decoration enhancement classes."""
        for element in soup.find_all(class_='decoration-enhanced'):
            current_classes = element.get('class', [])
            if 'decoration-enhanced' in current_classes:
                current_classes.remove('decoration-enhanced')
                if current_classes:
                    element['class'] = current_classes
                else:
                    del element['class']
    
    def _remove_decoration_meta_tags(self, soup: BeautifulSoup):
        """Remove decoration meta tags."""
        decoration_meta_names = [
            'decoration-theme',
            'decoration-version',
            'decoration-compatibility'
        ]
        
        for meta in soup.find_all('meta'):
            if meta.get('name') in decoration_meta_names:
                meta.decompose()
    
    def _generate_output_filename(self, original_path: Path, decoration_output: DecorationOutput) -> str:
        """Generate output filename for enhanced HTML."""
        theme_name = self._sanitize_filename(decoration_output.theme_config.name)
        stem = original_path.stem
        suffix = original_path.suffix
        
        return str(original_path.parent / f"{stem}_decorated_{theme_name}{suffix}")
    
    def _sanitize_filename(self, name: str) -> str:
        """Sanitize filename by removing invalid characters."""
        import re
        sanitized = re.sub(r'[^\w\-_\.]', '_', name)
        sanitized = re.sub(r'_+', '_', sanitized)
        return sanitized.strip('_') or 'theme'
    
    def validate_html_structure(self, html_file: str) -> Dict[str, any]:
        """
        Validate HTML structure for decoration compatibility.
        
        Args:
            html_file: Path to HTML file to validate
            
        Returns:
            Dictionary with validation results
        """
        html_path = Path(html_file)
        if not html_path.exists():
            return {'valid': False, 'error': 'File not found'}
        
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Check for required structure
            has_head = bool(soup.find('head'))
            has_body = bool(soup.find('body'))
            
            # Check for scroll-cast elements
            scroll_cast_elements = []
            selectors = [
                '.typewriter-char', '.typewriter-container', '.typewriter-sentence',
                '.railway-line', '.railway-container',
                '.scroll-line', '.scroll-container'
            ]
            
            for selector in selectors:
                class_name = selector[1:]
                elements = soup.find_all(class_=class_name)
                if elements:
                    scroll_cast_elements.append({
                        'selector': selector,
                        'count': len(elements)
                    })
            
            # Check for existing decorations
            has_existing_decoration = bool(
                soup.find_all(attrs={'data-decoration': 'emotional-decoration'})
            )
            
            return {
                'valid': True,
                'structure': {
                    'has_head': has_head,
                    'has_body': has_body,
                    'has_html_tag': bool(soup.find('html'))
                },
                'scroll_cast_elements': scroll_cast_elements,
                'has_existing_decoration': has_existing_decoration,
                'file_size': len(html_content),
                'encoding': 'utf-8'
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
    
    def preview_injection(
        self, 
        html_file: str, 
        decoration_output: DecorationOutput
    ) -> Dict[str, any]:
        """
        Preview what would be injected without actually modifying the file.
        
        Args:
            html_file: Path to HTML file
            decoration_output: Decoration to preview
            
        Returns:
            Dictionary with preview information
        """
        validation = self.validate_html_structure(html_file)
        if not validation['valid']:
            return validation
        
        # Calculate injection points and content
        css_size = len(decoration_output.css_content)
        js_size = len(decoration_output.js_content) if decoration_output.js_content else 0
        
        # Count elements that would be enhanced
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        soup = BeautifulSoup(html_content, 'html.parser')
        enhancement_targets = []
        
        selectors = [
            '.typewriter-char', '.typewriter-container', '.typewriter-sentence',
            '.railway-line', '.railway-container',
            '.scroll-line', '.scroll-container'
        ]
        
        for selector in selectors:
            class_name = selector[1:]
            elements = soup.find_all(class_=class_name)
            if elements:
                enhancement_targets.append({
                    'selector': selector,
                    'count': len(elements),
                    'would_be_enhanced': True
                })
        
        return {
            'valid': True,
            'preview': {
                'css_injection': {
                    'size_bytes': css_size,
                    'location': 'head',
                    'method': 'inline'
                },
                'js_injection': {
                    'size_bytes': js_size,
                    'location': 'body',
                    'method': 'inline',
                    'enabled': js_size > 0
                },
                'element_enhancements': enhancement_targets,
                'total_enhanced_elements': sum(t['count'] for t in enhancement_targets),
                'theme_name': decoration_output.theme_config.name,
                'estimated_size_increase': css_size + js_size
            }
        }