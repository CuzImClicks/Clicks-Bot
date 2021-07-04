import json

from aiohttp import ClientSession

from util import config


class PiHoleAPI:

    def __init__(self) -> None:
        self.url = f"http://{config.getPiHoleIp()}/admin/api.php?"

    @property
    def version(self) -> int:
        """[summary]

        Returns:
            int: [Returns the version of the API(2 or 3)]
        """
        async with ClientSession() as session:
            async with session.get(self.url+"version") as data:
                content = json.loads(data.text())["version"]
                return content

    @property
    def type(self) -> str:
        """[summary]

        Returns:
            str: [Return the backend used by the API(either PHP or FTL)]
        """
        async with ClientSession() as session:
            async with session.get(self.url+"type") as data:
                content = json.loads(data.text())["type"]
                return content

    @property
    def summaryRaw(self) -> dict:
        """[summary]

        Returns:
            dict: [Gives statistics in raw format(no number formatting applied)]
        """
        async with ClientSession() as session:
            async with session.get(self.url+"summaryRaw") as data:
                content = json.loads(data.text())
                return content

    @property
    def summary(self) -> dict:
        """[summary]

        Returns:
            dict: [Gives statistics in formatted style]
        """
        async with ClientSession() as session:
            async with session.get(self.url+"summary") as data:
                content = json.loads(data.text())
                return content

    @property
    def overTimeData10mins(self) -> dict:
        """[summary]

        Returns:
            dict: [Data needed for generating the domains/ads over time graph on the Pi-hole web dashboard]
        """
        async with ClientSession() as session:
            async with session.get(self.url+"overTimeData10mins") as data:
                content = json.loads(data.text())
                return content

    @property
    def topItems(self, item_amount: int) -> dict:
        """[summary]

        Args:
            item_amount (int): [Data needed for generating the Top Client list and Top Advertisers Lists]

        Returns:
            dict: [last n amount of queries]
        """
        async with ClientSession() as session:
            async with session.get(self.url+f"topItems={item_amount}") as data:
                content = json.loads(data.text())
                return content       

    @property
    def getQueryTypes(self) -> dict:
        """[summary]

        Returns:
            dict: [Shows number of queries that the Pi-hole's DNS server has processed]
        """
        async with ClientSession() as session:
            async with session.get(self.url+"getQueryTypes") as data:
                content = json.loads(data.text())
                return content

    @property
    def getAllQueries(self) -> dict:
        """[summary]

        Returns:
            dict: [First column: Timestring of query,
            Second column: Type of query(IPv4 or IPv6),
            Third column: Requested domain name,
            Fourth column: Requesting client,
            Fifth column: Answer type(1 = blocked by gravity.list, 2 = forwarded to upstream server, 3 = answered by local cache, 4 = blocked by wildcard blocking)]
        """
        async with ClientSession() as session:
            async with session.get(self.url+"getAllQueries") as data:
                content = json.loads(data.text())
                return content

    @property
    def recentBlocked(self) -> dict:
        """[summary]

        Returns:
            dict: [a list of recently blocked domains]
        """
        async with ClientSession() as session:
            async with session.get(self.url+"recentBlocked") as data:
                content = json.loads(data.text())
                return content
        



