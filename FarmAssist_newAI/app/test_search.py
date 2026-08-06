from search_engine import *



print("\n==============================")
print("MARKET SEARCH")
print("==============================")


markets_found = search_markets(
    "Tiruvallur"
)


for m in markets_found[:5]:

    print(
        m["market_name"],
        "-",
        m["shops"],
        "shops"
    )



print("\n==============================")
print("INFRA SEARCH")
print("==============================")


infra = search_infrastructure(
    "Theni"
)


for i in infra:

    print(
        "\nFacility :",
        i["facility"]
    )

    print(
        "District :",
        i["district"]
    )

    print(
        "Location :",
        i["location"]
    )

    print(
        "Benefit :",
        i["benefit"]
    )



print("\n==============================")
print("SCHEME SEARCH")
print("==============================")


scheme_results = search_schemes(
    "cold"
)


for s in scheme_results:

    print(
        "\nScheme :",
        s["scheme_name"]
    )

    print(
        s["description"][:200],
        "..."
    )