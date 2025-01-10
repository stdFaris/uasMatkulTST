from enum import Enum
class BookingType(str, Enum):
    HOURLY = "hourly"
    DAILY = "daily"
    MONTHLY = "monthly"


class PartnerRole(str, Enum):
    PEMBANTU = "pembantu"
    TUKANG_KEBUN = "tukang_kebun" 
    TUKANG_PIJAT = "tukang_pijat"
