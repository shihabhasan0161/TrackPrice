import csv
from get_price import get_price
from notifier import send_message as notify


def setup_csv(filename: str = "products.csv") -> None:
    """
    Sets up the products.csv file for storing product data.
    """

    data = []

    while True:
        link = input("Enter an Amazon or PlayStation store link (q to quit): ")
        print("Enter q to quit")
        if link == "" or link == "q":
            break

        price = get_price(link)
        if price is not None:
            name = link.split("/")[3].split("#")[0]
            print(f"Added {name}, current price: ${format(price, ',')}")
            notify(f"Added {name}, current price: ${format(price, ',')}")
            data.append([name, link, price])

    # write the name, link, price data into the products.csv file
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "link", "price(CAD)"])
        writer.writerows(data)

    print("CSV File Saved!")


def update_price(filename: str) -> None:
    """
    Updates the prices of the products in the products.csv file.
    """
    with open(filename, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        data = list(reader)

    prices = []
    for row in data:
        name, link, old_price = row
        price = get_price(link)
        if price is not None:
            prices.append((name, link, price))
            if price < float(old_price):
                print(
                    f"{link} is now ${format(price, ',')}, down from ${format(float(old_price), ',')}"
                )
                notify(
                    f"{link} is now ${format(price, ',')}, down from ${format(float(old_price), ',')}"
                )
            else:
                print(f"{link} is still ${format(price, ',')}")
                # if price is the same or higher, don't notify.
        else:
            print(f"Failed to retrieve price for {link}")
            notify(f"Failed to retrieve price for {link}")
            prices.append((name, link, old_price))


def main() -> None:
    try:
        update_price("products.csv")
    except FileNotFoundError:
        print("products.csv not found. run python local.py to setup.")
    setup_csv()


if __name__ == "__main__":
    main()
