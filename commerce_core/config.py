import os

# Path to the UCP CLI executable. Can be overridden with the UCP_CMD environment variable.
UCP_CMD = os.environ.get(
    'UCP_CMD',
    r'C:\Users\Waleed\AppData\Roaming\npm\ucp.cmd'
)

def get_ucp_cmd():
    """Return the configured UCP command path."""
    return UCP_CMD
