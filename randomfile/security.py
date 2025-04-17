from flask import Flask

def configure_security(app: Flask) -> None:
    """
    Configure security features for the Flask application.
    
    Args:
        app (Flask): The Flask application
    """
    # Register security middleware
    @app.after_request
    def add_security_headers(response):
        """Add security headers to all responses."""
        # Content Security Policy
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            "style-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "media-src 'self'"
        )
        
        # Prevent MIME type sniffing
        response.headers['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent clickjacking
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Enable XSS protection in browsers
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Strict Transport Security (if using HTTPS)
        if app.config.get('HTTPS_ENABLED', False):
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
    
    # Configure CSRF protection if using forms
    if app.config.get('WTF_CSRF_ENABLED', True):
        from flask_wtf.csrf import CSRFProtect
        csrf = CSRFProtect()
        csrf.init_app(app)