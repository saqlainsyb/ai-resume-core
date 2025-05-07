def escape_latex(text):
    """
    Escapes LaTeX special characters in user input.
    """
    if not isinstance(text, str):
        return text

    # Define replacements
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\textasciicircum{}',
        '\\': r'\textbackslash{}',
    }

    # Apply replacements
    for char, escaped in replacements.items():
        text = text.replace(char, escaped)

    return text
