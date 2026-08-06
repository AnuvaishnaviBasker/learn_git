import json
import os


# ===============================
# LOAD DATA
# ===============================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATA_DIR = os.path.join(
    BASE_DIR,
    "DATA"
)


def load_json(filename):

    path = os.path.join(
        DATA_DIR,
        filename
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)



markets = load_json(
    "markets.json"
)

schemes = load_json(
    "schemes.json"
)

infrastructure = load_json(
    "infrastructure.json"
)



# ===============================
# MARKET SEARCH
# ===============================


def search_markets(query):

    results = []

    query = query.lower()


    for market in markets:

        text = (
            str(market.get("district",""))
            +
            str(market.get("market_name",""))
        ).lower()


        if query in text:

            results.append(market)


    return results



# ===============================
# INFRASTRUCTURE SEARCH
# ===============================


def search_infrastructure(query):

    results=[]

    query=query.lower()


    for item in infrastructure:

        text = (
            str(item.get("district",""))
            +
            str(item.get("location",""))
            +
            str(item.get("facility",""))
        ).lower()


        if query in text:

            results.append(item)


    return results



# ===============================
# SCHEME SEARCH
# ===============================


def search_schemes(query):

    results=[]

    query=query.lower()


    for scheme in schemes:


        name = str(
            scheme.get(
                "scheme_name",
                ""
            )
        ).lower()


        description = str(
            scheme.get(
                "description",
                ""
            )
        ).lower()


        users = " ".join(
            scheme.get(
                "target_users",
                []
            )
        ).lower()



        if (
            query in name
            or query in description
            or query in users
        ):

            results.append(
                scheme
            )


    return results
