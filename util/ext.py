try:  # Assume IPython installed
    from IPython.core.display import display, clear_output, Markdown, HTML
except ImportError:  # Using simple text output
    display, clear_output, Markdown, HTML = print, None, None, None
