from src.logs.filter.filter_interface import IFilter  # Import the IFilter interface for consistency with the filtering framework.
import requests  # Import the requests library for making HTTP requests.

class RobotsCrawlers(IFilter):
    """
    A class to identify requests made by robots or crawlers based on their user agent.

    Attributes:
        custom_robots_list (list): A predefined list of known bot identifiers to check against.
        counter_robots_list (list): A dynamically downloaded list of bots from an external source.

    Methods:
        _download_robots_list():
            Downloads the COUNTER Robots list from an external source and updates the counter_robots_list attribute.
        filter(user_agent: str) -> str:
            Checks if the given user agent matches any known bot identifiers and returns the matched bot name.
    """

    # A predefined list of custom robot/crawler user-agent keywords.
    custom_robots_list = [
        "OAI-SearchBot", "ChatGPT-User", "GPTBot", "bingbot", "Mediapartners-Google*",
        "UbiCrawler", "DOC", "Zao", "sitecheck.internetseer.com", "Zealbot",
        "MSIECrawler", "SiteSnagger", "WebStripper", "WebCopier", "Fetch",
        "Offline Explorer", "Teleport", "TeleportPro", "WebZIP", "linko",
        "HTTrack", "Microsoft.URL.Control", "Xenu", "larbin", "libwww",
        "ZyBORG", "Download Ninja", "fast", "grub-client", "k2spider",
        "NPBot", "WebReaper", "AhrefsBot", "DataForSeoBot", "PetalBot",
        "ClaudeBot", "anthropic-ai", "Claude-Web"
    ]

    # An empty list to store dynamically fetched robot identifiers.
    counter_robots_list = []

    @classmethod
    def _download_robots_list(cls):
        """
        Downloads the COUNTER Robots list from a remote source and updates the `counter_robots_list` attribute.
        
        This method fetches a text file containing a list of known bot user agents and splits it into a list of strings.
        """
        # Check if the list is empty to avoid redundant downloads.
        if not cls.counter_robots_list:
            response = requests.get(
                'https://raw.githubusercontent.com/atmire/COUNTER-Robots/refs/heads/master/generated/COUNTER_Robots_list.txt'
            )
            # Populate the list with the downloaded data, splitting it by lines.
            cls.counter_robots_list = response.text.splitlines()

    @classmethod
    def filter(cls, user_agent: str) -> str:
        """
        Filters the user agent string to determine if it belongs to a known bot or crawler.

        Args:
            user_agent (str): The user agent string of the HTTP request.

        Returns:
            str: The name of the bot if identified; an empty string otherwise.
        """
        # Check against the predefined custom robots list.
        for bot_word in cls.custom_robots_list:
            if bot_word.lower() in user_agent.lower():  # Perform case-insensitive matching.
                return bot_word  # Return the matching bot name.

        # Download the COUNTER Robots list if not already done.
        cls._download_robots_list()

        # Check against the dynamically fetched robots list in reverse order.
        for bot_word in reversed(cls.counter_robots_list):
            if bot_word.lower() in user_agent.lower():  # Perform case-insensitive matching.
                return bot_word  # Return the matching bot name.

        return ""  # Return an empty string if no bot is identified.
