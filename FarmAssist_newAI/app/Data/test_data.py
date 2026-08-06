import json
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATA_DIR = os.path.join(
    BASE_DIR,
    "DATA"
)


files = [
    "markets.json",
    "schemes.json",
    "infrastructure.json"
]


for file in files:

    path = os.path.join(
        DATA_DIR,
        file
    )

    print("\nChecking:", path)


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)


    print(
        "Records:",
        len(data)
    )


    for item in data:

        for key, value in item.items():

            if str(value).lower() == "nan":

                print(
                    "Found NAN:",
                    item
                )
