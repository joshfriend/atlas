#!/usr/bin/env python

def slack_encode(string):
    """Escapes the three characters required by slack formatting:
    https://api.slack.com/docs/formatting#how_to_escape_characters
    """
    if string is None:
        return None
    return string.replace('&', '&amp') \
        .replace('<', '&lt') \
        .replace('>', '&gt')
