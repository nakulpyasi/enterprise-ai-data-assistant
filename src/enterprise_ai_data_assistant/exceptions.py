class FoundryServiceError(Exception):
    """Base exception for errors involving Azure AI Foundry."""


class FoundryTimeoutError(FoundryServiceError):
    """Raised when Foundry does not respond within the configured timeout."""


class FoundryUnavailableError(FoundryServiceError):
    """Raised when Foundry is unavailable, unreachable, or rate-limited."""


class FoundryResponseError(FoundryServiceError):
    """Raised when Foundry returns an empty or invalid response."""
    
class UnsafeSQLQueryError(Exception):
    """Raised when AI-generated SQL violates application safety rules.

    Examples:
    - DELETE or UPDATE instead of SELECT
    - Multiple SQL statements
    - Access to a table other than support_tickets
    """


class DatabaseQueryError(Exception):
    """Raised when PostgreSQL rejects or cannot execute a SQL query.

    Examples:
    - Invalid column name
    - Invalid PostgreSQL syntax
    - Another database execution error
    """


class DatabaseTimeoutError(Exception):
    """Raised when a database query exceeds the configured timeout."""


class DatabaseUnavailableError(Exception):
    """Raised when the application cannot connect to PostgreSQL."""
