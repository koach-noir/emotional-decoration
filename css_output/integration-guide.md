# Emotional Decoration Integration Guide

## Overview
This guide demonstrates how to integrate emotional-decoration CSS with scroll-cast HTML without modifying the core scroll-cast system.

## Integration Steps

### 1. Add CSS Import (AFTER scroll-cast styles)

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ScrollCast - TypeWriter Effect (Plugin)</title>
    
    <!-- ScrollCast Shared Styles (FIRST) -->
    <link rel="stylesheet" href="shared/scrollcast-styles.css">
    
    <!-- Emotional Decoration Enhancement (AFTER) -->
    <link rel="stylesheet" href="shared/emotional-decoration.css">
    
    <!-- ... rest of head ... -->
</head>
```

### 2. Optional: Add Enhancement Classes

For maximum effect, add `.decoration-enhanced` class to individual characters:

```html
<span class="typewriter-char decoration-enhanced" data-char-index="0" id="char-0">H</span>
```

### 3. CSS Override Architecture

The emotional-decoration CSS uses **CSS Override Architecture**:

- ✅ **Preserves** scroll-cast functionality (opacity, transition, display)
- ✅ **Enhances** visual appearance (background, filter, animation)  
- ✅ **No conflicts** with existing CSS selectors
- ✅ **Uses CSS custom properties** for easy customization

## Customization

Override CSS variables to customize the decoration:

```css
:root {
    --decoration-primary-start: #your-color;
    --decoration-primary-end: #your-color;
    --decoration-glow-intensity: 0.5;
    /* ... more variables ... */
}
```

## Architecture Benefits

1. **Non-interference**: Both systems work independently
2. **Backwards compatible**: Works with all existing scroll-cast HTML
3. **Optional**: Can be enabled/disabled without code changes
4. **Performance**: No impact on scroll-cast core functionality
5. **Maintainable**: Separate concerns and lifecycle

## Verification

To verify the integration works:

1. Scroll-cast animations function normally
2. Text gradients and glow effects are visible
3. No console errors or CSS conflicts
4. Responsive design works on mobile
5. Accessibility features remain intact

This integration demonstrates the "pre-agreed CSS/JS" approach where both systems prepare compatible files independently.
