import hashlib
import functools
import logging
from typing import Callable, Any, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)
logger = logging.getLogger("MedicalCLI")

def hash_password(password: str) -> str:
    """Simple SHA-256 hashing for password security."""
    return hashlib.sha256(password.encode()).hexdigest()

def log_action(func: Callable) -> Callable:
    """Decorator to log function calls."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Executing {func.__name__}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

def require_role(role: str):
    """Decorator to enforce role-based access control."""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # This is a placeholder for actual session-based auth
            # In a CLI, we might pass the user object in args
            user = kwargs.get('current_user')
            if not user:
                # Try to find user in positional args if not in kwargs
                for arg in args:
                    if hasattr(arg, 'role'):
                        user = arg
                        break
            
            if not user or user.role != role:
                print(f"Access Denied: Required role '{role}' not found.")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator
