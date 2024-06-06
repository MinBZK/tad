from typing import Literal

# TODO(berry): make enums and convert to types
EnvironmentType = Literal["local", "production", "demo"]
LoggingLevelType = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
DatabaseSchemaType = Literal["sqlite", "postgresql", "mysql", "oracle"]
