from dataclasses import dataclass

@dataclass
class Retailer:
    retailer_code: str
    retailer_name: str
    type: str
    country: str = None


