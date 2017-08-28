Bitly
=====

A block that creates a bitly url. Each input signal will be sent to output with the bitly link added on.

Properties
----------
- **api_key**: Bitly API Key.
- **bitly_link_attr**: Attribute to put bitly link on output signals. If unspecified, original link attribute is overridden.
- **link_attr**: Attribute of inputs signals that contains a link.

Inputs
------
- **default**: Any list of signals. They should contain the attribute specified in the property `link_signal_attribute (in)`.

Outputs
-------
- **default**: Input signals but with the attribute `link_signal_attribute (out)` set to the bitly link generated from the attribute `link_signal_attribute (in)`.

Commands
--------
None

Dependencies
------------
-   [requests](https://pypi.python.org/pypi/requests/)
