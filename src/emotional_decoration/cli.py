"""Command-line interface for emotional-decoration system."""

import click
import json
import sys
from pathlib import Path
from typing import Optional
from .models import DecorationRequest, ColorScheme, VisualEffect
from .orchestrator.decoration_engine import DecorationEngine


@click.group()
@click.version_option(version="1.0.0")
@click.option('--output-dir', default='decorations', help='Output directory for decorations')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def cli(ctx, output_dir: str, verbose: bool):
    """
    Emotional Decoration System - Visual enhancement for scroll-cast content.
    
    This tool analyzes text content and generates appropriate color schemes,
    gradients, and visual effects to enhance scroll-cast animations.
    """
    ctx.ensure_object(dict)
    ctx.obj['output_dir'] = output_dir
    ctx.obj['verbose'] = verbose
    ctx.obj['engine'] = DecorationEngine(output_dir)


@cli.command()
@click.argument('text', required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='Read text from file')
@click.option('--output', '-o', type=click.Path(), help='Output file for analysis results')
@click.option('--format', 'output_format', type=click.Choice(['json', 'text']), default='text', help='Output format')
@click.pass_context
def analyze(ctx, text: Optional[str], file: Optional[str], output: Optional[str], output_format: str):
    """
    Analyze text content for emotion, content type, and reading difficulty.
    
    Examples:
        emotional-decoration analyze "Hello World"
        emotional-decoration analyze --file content.txt
        emotional-decoration analyze "Learning content" --format json
    """
    engine = ctx.obj['engine']
    verbose = ctx.obj['verbose']
    
    # Get text input
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif not text:
        text = click.get_text_stream('stdin').read()
    
    if not text.strip():
        click.echo("Error: No text provided for analysis.", err=True)
        sys.exit(1)
    
    # Perform analysis
    if verbose:
        click.echo("Analyzing text content...")
    
    try:
        analysis_result = engine.analyze_text(text)
        
        if output_format == 'json':
            result_data = {
                'text_length': analysis_result.character_count,
                'word_count': analysis_result.word_count,
                'sentence_count': len(analysis_result.sentences),
                'processing_time': analysis_result.processing_time,
                'profile': {
                    'emotion': analysis_result.profile.emotion.value,
                    'emotion_intensity': analysis_result.profile.emotion_intensity,
                    'content_type': analysis_result.profile.content_type.value,
                    'difficulty': analysis_result.profile.difficulty.value,
                    'reading_speed': analysis_result.profile.reading_speed,
                    'recommended_theme': analysis_result.profile.recommended_theme,
                    'confidence': analysis_result.profile.confidence,
                    'key_themes': analysis_result.profile.key_themes
                },
                'keywords': analysis_result.keywords[:10]
            }
            
            result_json = json.dumps(result_data, indent=2)
            
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(result_json)
                click.echo(f"Analysis results saved to {output}")
            else:
                click.echo(result_json)
        else:
            # Text format output
            summary = engine.content_analyzer.get_analysis_summary(analysis_result)
            
            output_lines = [
                f"Analysis Results:",
                f"================",
                f"Text length: {summary['text_length']} characters",
                f"Word count: {summary['word_count']} words",
                f"Sentence count: {summary['sentence_count']} sentences",
                f"",
                f"Content Profile:",
                f"Primary emotion: {summary['primary_emotion']} (intensity: {summary['emotion_intensity']:.2f})",
                f"Content type: {summary['content_type']}",
                f"Difficulty level: {summary['difficulty']}",
                f"Reading speed: {summary['reading_speed']:.0f} words/min",
                f"Recommended theme: {summary['recommended_theme']}",
                f"Confidence: {summary['confidence']:.2f}",
                f"",
                f"Key themes: {', '.join(summary['key_themes'])}",
                f"Top keywords: {', '.join(summary['keywords'])}",
                f"",
                f"Processing time: {summary['processing_time']:.3f}s"
            ]
            
            result_text = "\\n".join(output_lines)
            
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(result_text)
                click.echo(f"Analysis results saved to {output}")
            else:
                click.echo(result_text)
                
    except Exception as e:
        click.echo(f"Error during analysis: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('text', required=False)
@click.option('--file', '-f', type=click.Path(exists=True), help='Read text from file')
@click.option('--template', '-t', type=click.Choice(['typewriter', 'railway', 'scroll']), default='typewriter', help='Target scroll-cast template')
@click.option('--theme', help='Theme preference (e.g., learning, professional, emotional)')
@click.option('--output', '-o', type=click.Path(), help='Output directory or filename prefix')
@click.option('--save', '-s', is_flag=True, help='Save decoration files')
@click.option('--name', help='Custom name for saved decoration')
@click.pass_context
def generate(ctx, text: Optional[str], file: Optional[str], template: str, theme: Optional[str], 
             output: Optional[str], save: bool, name: Optional[str]):
    """
    Generate decoration CSS/JS based on text analysis.
    
    Examples:
        emotional-decoration generate "Hello World" --template typewriter
        emotional-decoration generate --file content.txt --theme learning --save
        emotional-decoration generate "Story text" --template railway --name mystory
    """
    engine = ctx.obj['engine']
    verbose = ctx.obj['verbose']
    
    # Get text input
    if file:
        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif not text:
        text = click.get_text_stream('stdin').read()
    
    if not text.strip():
        click.echo("Error: No text provided for decoration generation.", err=True)
        sys.exit(1)
    
    # Generate decoration
    if verbose:
        click.echo(f"Generating decoration for {template} template...")
    
    try:
        decoration_output = engine.generate_theme_only(text, template, theme)
        
        if save:
            # Save decoration files
            file_paths = engine.save_decoration(decoration_output, name)
            
            click.echo("Decoration generated and saved:")
            for file_type, path in file_paths.items():
                click.echo(f"  {file_type}: {path}")
        else:
            # Output CSS to stdout or file
            if output:
                with open(output, 'w', encoding='utf-8') as f:
                    f.write(decoration_output.css_content)
                click.echo(f"CSS decoration saved to {output}")
            else:
                click.echo(decoration_output.css_content)
        
        if verbose:
            performance = decoration_output.performance_metrics
            click.echo(f"\\nPerformance metrics:")
            click.echo(f"  CSS size: {performance.get('css_size_bytes', 0)} bytes")
            click.echo(f"  CSS rules: {performance.get('css_rules_count', 0)}")
            click.echo(f"  CSS variables: {performance.get('css_variables_count', 0)}")
            
    except Exception as e:
        click.echo(f"Error during generation: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('html_file', type=click.Path(exists=True))
@click.argument('text', required=False)
@click.option('--text-file', type=click.Path(exists=True), help='Read text from file')
@click.option('--template', '-t', type=click.Choice(['typewriter', 'railway', 'scroll']), default='typewriter', help='Target scroll-cast template')
@click.option('--theme', help='Theme preference')
@click.option('--output', '-o', type=click.Path(), help='Output HTML file')
@click.option('--preview', '-p', is_flag=True, help='Preview decoration without applying')
@click.pass_context
def enhance(ctx, html_file: str, text: Optional[str], text_file: Optional[str], 
            template: str, theme: Optional[str], output: Optional[str], preview: bool):
    """
    Enhance existing HTML file with emotional decoration.
    
    Examples:
        emotional-decoration enhance base.html "Hello World"
        emotional-decoration enhance base.html --text-file content.txt --theme learning
        emotional-decoration enhance base.html "Story" --preview
    """
    engine = ctx.obj['engine']
    verbose = ctx.obj['verbose']
    
    # Get text input
    if text_file:
        with open(text_file, 'r', encoding='utf-8') as f:
            text = f.read()
    elif not text:
        text = click.get_text_stream('stdin').read()
    
    if not text.strip():
        click.echo("Error: No text provided for decoration analysis.", err=True)
        sys.exit(1)
    
    # Validate HTML compatibility
    if verbose:
        click.echo("Validating HTML compatibility...")
    
    validation = engine.validate_html_compatibility(html_file)
    if not validation['valid']:
        click.echo(f"Error: HTML file is not compatible: {validation.get('error', 'Unknown error')}", err=True)
        sys.exit(1)
    
    if preview:
        # Generate preview
        preview_data = engine.preview_decoration(html_file, text, template, theme)
        
        click.echo("Decoration Preview:")
        click.echo("==================")
        click.echo(f"Theme: {preview_data['preview']['theme_name']}")
        click.echo(f"Template: {template}")
        click.echo(f"Emotion: {preview_data['analysis']['emotion']}")
        click.echo(f"Content type: {preview_data['analysis']['content_type']}")
        click.echo(f"Difficulty: {preview_data['analysis']['difficulty']}")
        click.echo()
        click.echo("Changes that would be made:")
        click.echo(f"  CSS size: {preview_data['preview']['css_injection']['size_bytes']} bytes")
        click.echo(f"  JS size: {preview_data['preview']['js_injection']['size_bytes']} bytes")
        click.echo(f"  Elements enhanced: {preview_data['preview']['total_enhanced_elements']}")
        click.echo()
        click.echo("Enhanced element types:")
        for enhancement in preview_data['preview']['element_enhancements']:
            click.echo(f"  {enhancement['selector']}: {enhancement['count']} elements")
    else:
        # Apply enhancement
        if verbose:
            click.echo(f"Enhancing HTML file with {template} decoration...")
        
        try:
            enhanced_file = engine.enhance_html_file(html_file, text, output, template, theme)
            click.echo(f"Enhanced HTML saved to: {enhanced_file}")
            
        except Exception as e:
            click.echo(f"Error during enhancement: {e}", err=True)
            sys.exit(1)


@cli.command()
@click.pass_context
def list(ctx):
    """List all saved decorations."""
    engine = ctx.obj['engine']
    
    decorations = engine.list_decorations()
    
    if not decorations:
        click.echo("No saved decorations found.")
        return
    
    click.echo("Saved Decorations:")
    click.echo("==================")
    
    for decoration in decorations:
        click.echo(f"Name: {decoration['name']}")
        click.echo(f"  Theme: {decoration['theme_name']}")
        click.echo(f"  Description: {decoration['description']}")
        click.echo(f"  Compatible with: {', '.join(decoration['compatibility'])}")
        click.echo()


@cli.command()
@click.argument('name')
@click.option('--force', '-f', is_flag=True, help='Force deletion without confirmation')
@click.pass_context
def delete(ctx, name: str, force: bool):
    """Delete a saved decoration."""
    engine = ctx.obj['engine']
    
    if not force:
        if not click.confirm(f"Are you sure you want to delete decoration '{name}'?"):
            click.echo("Deletion cancelled.")
            return
    
    if engine.delete_decoration(name):
        click.echo(f"Decoration '{name}' deleted successfully.")
    else:
        click.echo(f"Error: Decoration '{name}' not found or could not be deleted.", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def stats(ctx):
    """Show system performance statistics."""
    engine = ctx.obj['engine']
    
    stats = engine.get_performance_stats()
    
    click.echo("System Performance Statistics:")
    click.echo("==============================")
    click.echo(f"Total requests processed: {stats['total_requests']}")
    click.echo(f"Total processing time: {stats['total_processing_time']:.3f}s")
    click.echo(f"Average processing speed: {stats['average_chars_per_second']:.0f} chars/sec")
    click.echo()
    click.echo("Cache Statistics:")
    click.echo(f"  Cached analyses: {stats['cache_stats']['cache_size']}")
    click.echo(f"  Total cached characters: {stats['cache_stats']['total_cached_chars']}")
    click.echo()
    click.echo("System Status:")
    for component, status in stats['system_info'].items():
        status_text = "✓" if status else "✗"
        click.echo(f"  {component}: {status_text}")


@cli.command()
@click.pass_context
def clear_cache(ctx):
    """Clear all system caches."""
    engine = ctx.obj['engine']
    
    engine.clear_caches()
    click.echo("All caches cleared successfully.")


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()