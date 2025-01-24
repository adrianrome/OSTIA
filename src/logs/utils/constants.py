# Constants for labels and log counters, used throughout the project for log processing and categorization.

LABEL_VALUE = "value"  # Key name for a generic label value.

# Constants for label types, categorizing different types of logs or resources.
LABEL_TYPE = "type"  # Key name for a log's type.
LABEL_TYPE_SEARCH = "cerca"  # Label type for search-related logs.
LABEL_TYPE_OTHERS = "altres"  # Label type for logs categorized as 'others'.
LABEL_TYPE_RESOURCE = "recurs"  # Label type for general resource-related logs.
LABEL_TYPE_RESOURCE_BITSTREAM = "recurs-bitstream"  # Label type for bitstream-related resources.
LABEL_TYPE_RESOURCE_WEB = "recurs-web"  # Label type for web resource-related logs.
LABEL_TYPE_BITSTREAM = "bitstream"  # Label type for logs specific to bitstreams.

# Constants for content labels, representing the outcome or content of the log.
LABEL_CONTENT = "content"  # Key name for a log's content type.
LABEL_CONTENT_OK = "ok"  # Content label indicating a successful operation.
LABEL_CONTENT_ERROR = "error"  # Content label indicating an error in the operation.
LABEL_CONTENT_DIFFERENT = "diferent"  # Content label indicating a discrepancy or difference.

# Constants for log counters, used for tracking various log statistics.
LOG_COUNTER = "counter"  # General log counter key.
LOG_COUNTER_STATUS_CODE = "status_code_counter"  # Counter for tracking HTTP status codes.
LOG_COUNTER_DOUBLE_CLICK = "double_click_counter"  # Counter for tracking double-click events.
LOG_COUNTER_ROBOTS_CRAWLERS = "robots_crawlers_counter_total"  # Total counter for robots and crawlers.
LOG_COUNTER_ROBOTS_CRAWLERS_BREAKDOWN = "robots_crawlers_counter_breakdown"  # Detailed counter for individual robots/crawlers.
