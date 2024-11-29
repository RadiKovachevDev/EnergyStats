from .models import HourlyData, HourlyInfo
import requests
from .models import LatestPriceDate, EnergyPrice
from datetime import datetime
from decouple import config


def fetch_prices():
    print("fetch_prices started")
    url = config("API_URL_PRICES")
    print(f"Fetching data from {url}")
    response = requests.get(url)
    print(f"HTTP Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        for item in data:
            energy_price, created = EnergyPrice.objects.get_or_create(
                _id=item["_id"],
                defaults={
                    "date": datetime.strptime(item["date"], "%d.%m.%Y").date()
                }
            )

            for hourly in item["hourlyData"]:
                hourly_info, info_created = HourlyInfo.objects.get_or_create(
                    eur=hourly["data"]["eur"],
                    bgn=hourly["data"]["bgn"],
                    volume=hourly["data"]["volume"]
                )

                hourly_data, data_created = HourlyData.objects.get_or_create(
                    time=hourly["time"],
                    data=hourly_info
                )

                if data_created:
                    energy_price.hourly_data.add(hourly_data)


def fetch_latest_price():
    url = config("API_URL_LATEST_PRICE")

    print(f"Fetching data from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "data" in data and isinstance(data["data"], dict):
            nested_data = data["data"]
            HourlyInfo.objects.create(
                eur=nested_data.get("eur"),
                bgn=nested_data.get("bgn"),
                volume=nested_data.get("volume")
            )


def fetch_latest_price_date():
    url = config("API_URL_LATEST_PRICE_DATE")
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        latest_date_str = data.get("latest date")
        if latest_date_str:
            latest_date = datetime.strptime(latest_date_str, "%d.%m.%Y").date()
            LatestPriceDate.objects.update_or_create(
                latest_date=latest_date
            )
            return latest_date
        else:
            print("No 'latest date' found in the response.")
            return None
    else:
        print(f"Failed to fetch latest price date: {response.status_code}")
        return None


def should_fetch_prices():
    url = config("API_URL_LATEST_PRICE_DATE")

    print(f"Fetching data from {url}")
    response = requests.get(url)
    if response.status_code == 200:
        latest_api_date = response.json().get("latest date")
        if not latest_api_date:
            return False

        latest_api_date = datetime.strptime(latest_api_date, "%d.%m.%Y").date()

        latest_db_date = LatestPriceDate.objects.order_by('-latest_date').first()

        if latest_db_date and latest_db_date.latest_date == latest_api_date:
            return False

        LatestPriceDate.objects.create(latest_date=latest_api_date)
        return True

    print(f"Failed to fetch latest date: {response.status_code}")
    return False


def update_prices():
    print("update")
    fetch_prices()
