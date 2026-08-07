"""
List of trusted news source keywords.

If any of these keywords are found in an article's source string,
the article will be marked as coming from a trusted source.
"""

TRUSTED_SOURCES = {
    # International News Agencies
    "reuters",
    "associated press",
    "ap",

    # International News Organizations
    "bbc",
    "cnn",
    "bloomberg",
    "the guardian",
    "guardian",
    "financial times",
    "the economist",
    "npr",
    "usa today",

    # Newspapers
    "new york times",
    "nyt",
    "washington post",
    "wall street journal",
    "wsj",

    # Television Networks
    "abc",
    "abc news",
    "cbs",
    "cbs news",
    "nbc",
    "nbc news",

    # International
    "al jazeera",
    "al jazeera english",
    "dw",
    "deutsche welle",
    "france 24",
    "euronews",

    # Technology
    "techcrunch",
    "the verge",
    "wired",
    "ars technica",

    # Business
    "forbes",
    "fortune",
    "business insider",
    "marketwatch",
    "cnbc",

    # Science
    "nature",
    "science",
    "scientific american",
}