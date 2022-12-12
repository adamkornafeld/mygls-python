from enum import Enum
from pydantic import BaseSettings


class CountryCode(Enum):
    HU = "hu"
    HR = "hr"
    CZ = "cz"
    RO = "ro"
    SI = "si"
    SK = "sk"


class Settings(BaseSettings):
    country: CountryCode = CountryCode.HU
    test: bool = False
    timeout_seconds: int = 5

    @property
    def api_root(self):
        test = ".test" if self.test else ""
        return f"https://api{test}.mygls.{self.country.value}/ParcelService.svc/json"
