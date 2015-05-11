===============================
logaway
===============================

.. image:: https://img.shields.io/travis/petri/logaway.svg
        :target: https://travis-ci.org/petri/logaway

.. image:: https://img.shields.io/pypi/v/logaway.svg
        :target: https://pypi.python.org/pypi/logaway


Provides throwaway, in-browser log events display for use with the Python stdlib UDP log
handler (logging.handlers.DatagramHandler).

Start up a crossbar (http://crossbar.io) router, run the udp-log-receiver and off you go:

.. code-block:: python
    import logging
    from logging.handlers import DatagramHandler


    logging.basicConfig()
    logger = logging.getLogger("logreceiver")
    handler = DatagramHandler("127.0.0.1", 9999)
    logger.addHandler(handler)

    if __name__ == "__main__":
       logger.warn("TEST")


Use https://docs.python.org/2/library/logging.handlers.html#datagramhandler to log to
this tool.


* Free software: BSD license
* Documentation: https://logaway.readthedocs.org.

Features
--------

* TODO
