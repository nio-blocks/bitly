Bitly
===========

A block that creates a bitly url. Each input signal will be sent to output with the bitly link added on.

Properties
--------------

-   **link_signal_attribute - in**: Attribute of inputs signals that contains a link.
-   **link_signal_attribute - out**: Attribute to put bitly link on output signals. If unspecified, original link attribute is overridden.
-   **api_key**: Bitly API Key.

Dependencies
----------------

-   [requests](https://pypi.python.org/pypi/requests/)

Commands
----------------
None

Input
-------
Any list of signals. They should contain the attribute specified in the property `link_signal_attribute (in)`.

Output
---------
Input signals but with the attribute `link_signal_attribute (out)` set to the bitly link generated from the attribute `link_signal_attribute (in)`.
