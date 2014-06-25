Bitly
===========

A block that creates a bitly url. Each input signal will be sent to output with the bitly link added on.

Properties
--------------

-   **Link Signal Attribute (in)**: Attribute of inputs signals that contains a link.
-   **Link Signal Attribute (out)**: Attribute to put bitly link on output signals. If unspecified, original link attribute is overridden.
-   **API Key**: Bitly API Key.

Dependencies
----------------

-   [requests](https://pypi.python.org/pypi/requests/)

Commands
----------------
None

Input
-------
Any list of signals. They should contain the attribute specifeid in the property *Link Signal Attribute (in)*.

Output
---------
Input signals but with the attribute *Link Signal Attrubute (out)* set to the bitly link generated from the attribute *Link Signal Attribute (in)*.
