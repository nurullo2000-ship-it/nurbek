"""
Schema generation hooks for drf-spectacular
"""

def preprocessing_filter_hook(endpoints):
    """
    Filter endpoints for API schema generation
    """
    filtered = []
    for path, path_regex, method, view in endpoints:
        if path.startswith('/api/'):
            filtered.append((path, path_regex, method, view))
    return filtered
