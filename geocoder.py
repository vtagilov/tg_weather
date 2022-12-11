import requests
from dataclasses import dataclass

ADDRESS_API = "https://nominatim.openstreetmap.org/search/{title}?format=json"


@dataclass(slots=True, frozen=True)
class Address:
    latitude: float
    longitude: float
    title: str


def get_position_api(title) -> Address:
    address_data = requests.get(ADDRESS_API.format(title=title)).json()
    print(address_data[0]["lat"], address_data[0]["lon"])
    return Address(
        latitude=address_data[0]["lat"],
        longitude=address_data[0]["lon"],
        title=address_data[0]["display_name"]
    )
