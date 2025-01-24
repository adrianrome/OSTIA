# Regex pattern for extracting resource identifiers.

HANDLE = r'((2099(.[1-4])?|2117)\/\d+)'
"""
str: A regular expression pattern used to match resource identifiers.

This pattern is designed to capture resource identifiers that follow the format:
- A prefix (e.g., `2099` or `2117`), optionally followed by `.1`, `.2`, `.3`, or `.4`.
- A forward slash (`/`).
- A numeric identifier (e.g., `12345`).

Examples of matching resource identifiers:
- `2099/12345`
- `2117/67890`
- `2099.1/54321`

The `HANDLE` pattern is commonly used to extract resource identifiers from metadata or resource strings.
"""
