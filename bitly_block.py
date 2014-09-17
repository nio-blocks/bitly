from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties.string import StringProperty

import requests
import urllib

BITLY_SHORTEN_URL = "https://api-ssl.bitly.com" + \
                    "/v3/shorten?access_token=%s&longUrl=%s"


@Discoverable(DiscoverableType.block)
class Bitly(Block):

    """ A block that create a bitly url.

    Properties:
        api_key (str): Bitly API Key.
        link_attr (str): Signal attribute with link.
        bitly_link_attr (str): Signal attribute to put Bitly
            link. If unspecified, overwrite original link attr.

    """

    api_key = StringProperty(tile="API Key")
    link_attr = StringProperty(title="Link Signal Attribute (in)",
                               default="link")
    bitly_link_attr = StringProperty(title="Link Signal Attribute (out)",
                                     allow_none=True)

    def process_signals(self, signals):
        for sig in signals:
            if not hasattr(sig, self.link_attr):
                self._logger.warning("Signal has no attribute %s" %
                                     self.link_attr)
                continue

            old_link = getattr(sig, self.link_attr)
            url = BITLY_SHORTEN_URL % (
                self.api_key, urllib.parse.quote_plus(old_link))
            data = self._get_bitly_response(url)
            if not data:
                # Bad response form bitly but save off old link
                # to new link signal attr anyway.
                self._set_new_attr(sig, old_link)
                continue

            new_link = old_link
            try:
                new_link = data["data"]["url"]
                self._logger.debug("New link is %s" % new_link)
            except (KeyError, TypeError):
                self._logger.warning("Could not extract url from response")
                self._logger.debug(data)

            self._set_new_attr(sig, new_link)

        self.notify_signals(signals)

    def _get_bitly_response(self, url):
        """Returns bitly json response or None if invalid url."""

        self._logger.debug("Trying to get %s" % url)
        resp = requests.get(url)

        if resp.status_code != 200:
            self._logger.error("Bitly request returned %s" %
                               resp.status_code)
            return

        data = resp.json()
        self._logger.debug(data)
        return data

    def _set_new_attr(self, sig, link):
        new_attr = self.bitly_link_attr or self.link_attr
        setattr(sig, new_attr, link)
