import pyfiglet
from show_listings import show_listings
from watchlist import show_watchlist

ascii_banner = pyfiglet.figlet_format("NEX Terminal")
print(ascii_banner)
while True:
    print("Main Menu:",end="")
    print("""
    1. Show listings (First Filter)
    2. Show Watchlist
          """)
    try:
        option = int(input("[Select]: "))
        if option == 1:
            show_listings()
        elif option == 2:
            show_watchlist()
    except ValueError as e:
        pass
