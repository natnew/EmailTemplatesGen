"""Decorators for logging and error handling."""

import functools
import time
from typing import Callable, Any, Optional

from email_templates_gen.utils.logging_config import get_logger
from email_templates_gen.utils.error_handler import APIError


def log_function_call(logger_name: Optional[str] = None):
    """Decorator to log function entry and exit with timing.
    
    Args:
        logger_name: Optional logger name, defaults to function's module
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = get_logger(logger_name or func.__module__)
            start_time = time.time()
            
            logger.info(
                "Function called",
                function=func.__name__,
                args_count=len(args),
                kwargs_keys=list(kwargs.keys()),
            )
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(
                    "Function completed successfully",
                    function=func.__name__,
                    duration_seconds=duration,
                )
                return result
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "Function failed",
                    function=func.__name__,
                    duration_seconds=duration,
                    error=str(e),
                    error_type=type(e).__name__,
                    exc_info=True,
                )
                raise
        return wrapper
    return decorator


def log_api_call(service: str):
    """Decorator to log API calls with timing and error handling.
    
    Args:
        service: Name of the external service being called
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = get_logger("api_calls")
            start_time = time.time()
            
            logger.info(
                "API call started", 
                service=service, 
                function=func.__name__,
                args_count=len(args),
                kwargs_keys=list(kwargs.keys()),
            )
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                logger.info(
                    "API call successful",
                    service=service,
                    function=func.__name__,
                    duration_seconds=duration,
                )
                return result
            except APIError as e:
                duration = time.time() - start_time
                logger.error(
                    "API call failed",
                    service=service,
                    function=func.__name__,
                    duration_seconds=duration,
                    error=str(e),
                    status_code=e.status_code,
                    details=e.details,
                )
                raise
            except Exception as e:
                duration = time.time() - start_time
                logger.error(
                    "API call failed with unexpected error",
                    service=service,
                    function=func.__name__,
                    duration_seconds=duration,
                    error=str(e),
                    error_type=type(e).__name__,
                    exc_info=True,
                )
                raise APIError(service, f"Unexpected error: {e}")
        return wrapper
    return decorator


def handle_errors(
    default_return=None,
    exceptions_to_catch: tuple = (Exception,),
    logger_name: Optional[str] = None,
):
    """Decorator to handle and log exceptions with optional default return.
    
    Args:
        default_return: Value to return if an exception is caught
        exceptions_to_catch: Tuple of exception types to catch
        logger_name: Optional logger name
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = get_logger(logger_name or func.__module__)
            
            try:
                return func(*args, **kwargs)
            except exceptions_to_catch as e:
                logger.error(
                    "Function error handled",
                    function=func.__name__,
                    error=str(e),
                    error_type=type(e).__name__,
                    exc_info=True,
                )
                return default_return
        return wrapper
    return decorator


def retry_on_failure(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions_to_retry: tuple = (Exception,),
):
    """Decorator to retry function calls on failure with exponential backoff.
    
    Args:
        max_retries: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff_factor: Factor to multiply delay by for each retry
        exceptions_to_retry: Tuple of exception types to retry on
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = get_logger("retry")
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions_to_retry as e:
                    if attempt == max_retries:
                        logger.error(
                            "Function failed after all retries",
                            function=func.__name__,
                            attempt=attempt + 1,
                            max_retries=max_retries,
                            error=str(e),
                        )
                        raise
                    
                    wait_time = delay * (backoff_factor ** attempt)
                    logger.warning(
                        "Function failed, retrying",
                        function=func.__name__,
                        attempt=attempt + 1,
                        max_retries=max_retries,
                        retry_delay=wait_time,
                        error=str(e),
                    )
                    time.sleep(wait_time)
            
        return wrapper
    return decorator
