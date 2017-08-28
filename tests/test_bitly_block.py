from unittest.mock import MagicMock

from nio.testing.block_test_case import NIOBlockTestCase
from nio.signal.base import Signal
from nio.block.terminals import DEFAULT_TERMINAL

from ..bitly_block import Bitly


class LinkSignal(Signal):
    def __init__(self, link):
        super().__init__()
        self.link = link


class TestBitly(NIOBlockTestCase):

    def test_bitly(self):
        link = "http://google.com"
        bitly_link = "http://b.n.io/sample"
        block = Bitly()
        block._get_bitly_response = MagicMock(
            return_value={'status_txt': 'OK',
                          'data': {'global_hash': 'LmvF',
                                   'new_hash': 0,
                                   'url': bitly_link,
                                   'hash': '1nPtHPq',
                                   'long_url': link},
                          'status_code': 200}
        )
        config = {"api_key": "1234567890",
                  "link_attr": "link"}
        self.configure_block(block, config)
        block.start()
        block.process_signals([LinkSignal(link)])
        self.assert_num_signals_notified(1)
        # assert link is updated to bitly_link.
        self.assertEqual(bitly_link,
                         self.last_notified[DEFAULT_TERMINAL][0].link)
        block.stop()

    def test_bitly_link_attr(self):
        link = "http://google.com"
        bitly_link = "http://b.n.io/sample"
        block = Bitly()
        block._get_bitly_response = MagicMock(
            return_value={'status_txt': 'OK',
                          'data': {'global_hash': 'LmvF',
                                   'new_hash': 0,
                                   'url': bitly_link,
                                   'hash': '1nPtHPq',
                                   'long_url': link},
                          'status_code': 200}
        )
        config = {"api_key": "1234567890",
                  "bitly_link_attr": "new_link",
                  "link_attr": "link"}
        self.configure_block(block, config)
        block.start()
        block.process_signals([LinkSignal(link)])
        self.assert_num_signals_notified(1)
        # assert bitly_link_attr is updated to new link.
        self.assertEqual(bitly_link,
                         self.last_notified[DEFAULT_TERMINAL][0].new_link)
        # assert original link attr is unchanged.
        self.assertEqual(link, self.last_notified[DEFAULT_TERMINAL][0].link)
        block.stop()

    def test_bad_link_attr(self):
        link = "http://google.com"
        bitly_link = "http://b.n.io/sample"
        link_attr = "bad_link_attr"
        bitly_link_attr = "bitly_link"
        block = Bitly()
        block._get_bitly_response = MagicMock(
            return_value={'status_txt': 'OK',
                          'data': {'global_hash': 'LmvF',
                                   'new_hash': 0,
                                   'url': bitly_link,
                                   'hash': '1nPtHPq',
                                   'long_url': link},
                          'status_code': 200}
        )
        config = {"api_key": "1234567890",
                  "bitly_link_attr": bitly_link_attr,
                  "link_attr": link_attr}
        self.configure_block(block, config)
        block.start()
        block.process_signals([LinkSignal(link)])
        self.assert_num_signals_notified(1)
        # assert original link attr is unchanged.
        self.assertEqual(link, self.last_notified[DEFAULT_TERMINAL][0].link)
        block.stop()

    def test_bad_api_key(self):
        link = "http://google.com"
        block = Bitly()
        block._get_bitly_response = MagicMock(return_value=None)
        config = {"api_key": "1234567890",
                  "link_attr": "link"}
        self.configure_block(block, config)
        block.start()
        block.process_signals([LinkSignal(link)])
        self.assert_num_signals_notified(1)
        # assert link is unchanged.
        self.assertEqual(link, self.last_notified[DEFAULT_TERMINAL][0].link)
        block.stop()

    def test_bad_api_key_with_bitly_link_attr(self):
        link = "http://google.com"
        block = Bitly()
        block._get_bitly_response = MagicMock(return_value=None)
        config = {"api_key": "1234567890",
                  "bitly_link_attr": "new_link",
                  "link_attr": "link"}
        self.configure_block(block, config)
        block.start()
        block.process_signals([LinkSignal(link)])
        self.assert_num_signals_notified(1)
        # assert link is unchanged.
        self.assertEqual(link, self.last_notified[DEFAULT_TERMINAL][0].link)
        # assert bitly_link_attr is set to original link.
        self.assertEqual(link,
                         self.last_notified[DEFAULT_TERMINAL][0].new_link)
        block.stop()
