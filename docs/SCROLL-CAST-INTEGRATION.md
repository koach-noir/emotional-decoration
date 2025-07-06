# ScrollCast Integration Guide

## Overview

This document describes the integration between the **emotional-decoration** system and **scroll-cast** templates using the Template-Based Architecture with common selectors.

## Architecture

### Common Selector System

The Template-Based Architecture migration enables both systems to use unified HTML structure:

```html
<div class="text-container" data-template="railway">
    <div class="text-line" data-line="0">Text content here</div>
    <div class="text-line" data-line="1">More text content</div>
</div>
```

### Supported Templates

- **Railway Template**: `data-template="railway"`
- **Scroll Template**: `data-template="scroll"`

## CSS Enhancement Files

### 1. `text-color-simple.css`
Basic text color enhancements for immediate use:
- Railway: Green station display style (#00ff88)
- Scroll: Golden movie credits style (#ffd700)
- Active states: Enhanced white with glow effects

### 2. `scroll-cast-text-color-enhancement.css`
Comprehensive enhancement system featuring:
- Template-specific color schemes
- Emotional layer support (`data-emotion="positive|negative|neutral|excited"`)
- Content-based variations
- Line progression effects
- Accessibility support

## Integration Method

### Non-Interference Design (お互いの生成物は干渉しない設計)

The emotional-decoration CSS follows strict non-interference principles:

✅ **ALLOWED:**
- Color modifications
- Text-shadow effects
- CSS transitions for color/shadow only

❌ **FORBIDDEN:**
- Layout modifications (position, display, transform)
- Animation timing changes
- Core scroll-cast functionality interference

### CSS Override Architecture

```css
/* ✅ Correct: Additive enhancement */
.text-container[data-template="railway"] .text-line {
    color: #00ff88;
    text-shadow: 0 0 8px rgba(0, 255, 136, 0.4);
}

/* ❌ Incorrect: Would interfere with animations */
.text-container .text-line {
    position: absolute; /* Never modify layout */
    opacity: 0.5;       /* Never modify core animations */
}
```

## Usage Examples

### Basic Implementation

Include the simple enhancement CSS:

```html
<link rel="stylesheet" href="emotional-decoration/css/text-color-simple.css">
```

### Advanced Implementation

Include the comprehensive enhancement system:

```html
<link rel="stylesheet" href="emotional-decoration/css/scroll-cast-text-color-enhancement.css">
```

Add emotional data attributes:

```html
<div class="text-container" data-template="railway" data-emotion="positive">
    <div class="text-line" data-line="0">Happy content</div>
</div>
```

### Dynamic Integration

For programmatic control:

```javascript
// Enable enhancement
document.body.classList.add('emo-deco-enhanced');

// Set emotional context
container.setAttribute('data-emotion', 'excited');

// Template switching
container.setAttribute('data-template', 'scroll');
```

## Testing

### Visual Testing

Use the provided demo file:
```
emotional-decoration/demo/scroll-cast-integration-demo.html
```

### Integration Testing

1. Generate scroll-cast HTML templates
2. Include emotional-decoration CSS
3. Verify:
   - Colors are applied correctly
   - Animations work normally
   - No layout interference
   - Accessibility compliance

## Performance Considerations

### Minimal Impact
- Pure CSS implementation
- No JavaScript required
- Selective targeting with data attributes
- Efficient CSS selectors

### Optimization
- Uses hardware-accelerated properties only
- Respects `prefers-reduced-motion`
- Fallbacks for high-contrast mode
- Print-friendly styles

## Browser Support

- **Modern browsers**: Full feature support
- **IE11+**: Basic color support
- **Mobile**: Full responsive support
- **Accessibility**: Screen reader compatible

## Future Enhancements

### Planned Features
- Color palette expansion
- Animation synchronization
- Dynamic emotion detection
- Theme system integration

### Extension Points
- Custom emotion categories
- Template-specific enhancements
- User preference integration
- Analytics integration

## Troubleshooting

### Common Issues

**Colors not applying:**
- Check CSS file inclusion
- Verify data-template attributes
- Check CSS specificity conflicts

**Animation interference:**
- Review CSS for layout properties
- Check for opacity/transform modifications
- Validate selector specificity

**Performance issues:**
- Verify hardware acceleration usage
- Check for redundant CSS rules
- Monitor animation frame rates

## Technical Specifications

### CSS Custom Properties Support
```css
.text-container {
    --emo-primary-color: #00ff88;
    --emo-glow-intensity: 0.4;
    --emo-transition-speed: 0.3s;
}
```

### Selector Patterns
```css
/* Template targeting */
.text-container[data-template="railway"]

/* Line targeting */
.text-line[data-line="0"]

/* State targeting */
.text-line.fade-in

/* Emotion targeting */
.text-container[data-emotion="positive"]
```

## Conclusion

The emotional-decoration system provides seamless, non-intrusive enhancement of scroll-cast templates through the Template-Based Architecture. The common selector system enables powerful decoration capabilities while maintaining strict separation of concerns and performance optimization.