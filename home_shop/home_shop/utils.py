def action(description):
    def decorator(func):
        func.short_description = description
        return func
    return decorator