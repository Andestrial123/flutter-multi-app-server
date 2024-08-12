import enum


class Unit(str, enum.Enum):
    piece = "piece"
    gram = "gram"


class DiscountOpenType(str, enum.Enum):
    web_view = "web_view"
    browser = "browser"
    browser_tab = "browser_tab"
    deeplink = "deeplink"
