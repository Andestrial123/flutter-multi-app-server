import enum


class Unit(str, enum.Enum):
    piece = "piece"
    gram = "gram"


class DiscountOpenType(str, enum.Enum):
    web_view = "web_view"
    browser = "browser"
    browser_tab = "browser_tab"
    deeplink = "deeplink"


class Day(enum.Enum):
    monday = "monday"
    tuesday = "tuesday"
    wednesday = "wednesday"
    thursday = "thursday"
    friday = "friday"
    saturday = "saturday"
    sunday = "sunday"


class WorkType(str, enum.Enum):
    default = "default"
    delivery = "delivery"


class LanguageCode(str, enum.Enum):
    en = "en"
    uk = "uk"
