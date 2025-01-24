# Regex pattern for matching IPv6 addresses in logs.
IPV6_PATTERN = r"^([a-fA-F0-9:]+|[uU]nknown), "
# Matches an IPv6 address at the start of a log or the literal 'unknown', followed by a comma.

# Regex pattern for identifying web resources with specific file extensions.
WEB_EXTENSIONS = r'.*\.(js|woff|jpg|css|png(.*)?|ico|txt|gif)$'
# Matches URLs that end with common static web resource extensions, such as JavaScript, images, stylesheets, etc.

# Regex pattern for matching handle identifiers in URLs, excluding bitstream paths.
HANDLE = r'(?<!/bitstream)/handle/((2099(.[1-4])?|2117)\/\d+)'
# Matches DSpace handle identifiers (e.g., '2117/12345'), excluding those in a bitstream path.

# Regex pattern for matching handle identifiers specifically in bitstream paths.
HANDLE_BITSTREAM = r'(?<=/bitstream/handle/)((2099(.[1-4])?|2117)\/\d+)'
# Matches DSpace handle identifiers in URLs that include '/bitstream/handle/'.

# Regex pattern for extracting bitstream IDs from a URL.
BITSTREAM = r'bitstream\/id\/([^\/]*)\/'
# Captures the bitstream ID from a URL, which appears after 'bitstream/id/'.

# List of search-related keywords used for identifying search actions in logs.
SEARCH_KEYS = [
    'discover?', 'scholar?', 'examens?',          # Keywords for general searches and scholarly content.
    'browse?', 'browse-', '-search?', 'search?',  # Keywords related to browsing and search actions.
    'search-filter?',                             # Keyword for filtered searches.
    'community?', 'community-list',              # Keywords related to community-based content.
    'item?', 'items-by-', 'items-by-',            # Keywords for accessing items and their categorizations.
    'fonsantic?', 'llibres?', 'video?', 'videos?', # Keywords for specific content types like books and videos.
    'e-prints', 'eprintsrecercat?', 'revistes?', 'tesis'  # Keywords for repositories, journals, and theses.
]
# SEARCH_KEYS is used to identify log entries that relate to specific search or content access actions.
