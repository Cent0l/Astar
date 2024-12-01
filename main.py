import heapq
import math
# Ładne kolorki
from colorama import init, Fore

# tu colorama dziala
init(autoreset=True)

# Wczytanie mapy z pliku (ten sam folder!!!)
def wczytaj_mape(nazwa_pliku):
    with open(nazwa_pliku, 'r') as plik:
        return [list(map(int, linia.strip().split())) for linia in plik]

# odleglosc
def odleglosc(x, y, cel):
    return math.sqrt((x - cel[0]) ** 2 + (y - cel[1]) ** 2)

# Funkcja
def a_star(mapa, start, cel):
    kolejka = [(0, start)]
    heapq.heapify(kolejka)

    koszty = {start: 0}
    rodzice = {start: None}
    sciezka = []

    while kolejka:
        obecny_koszt, obecny = heapq.heappop(kolejka)

        if obecny == cel:
            sciezka = odtworz_sciezke(mapa, rodzice, cel)
            break

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            sasiad = (obecny[0] + dx, obecny[1] + dy)
            if czy_valid(mapa, sasiad):
                nowy_koszt = koszty[obecny] + 1
                if sasiad not in koszty or nowy_koszt < koszty[sasiad]:
                    koszty[sasiad] = nowy_koszt
                    priorytet = nowy_koszt + odleglosc(*sasiad, cel)
                    heapq.heappush(kolejka, (priorytet, sasiad))
                    rodzice[sasiad] = obecny

    return sciezka, koszty[cel]  # Ścieżka i koszt w jedna strone

# Funkcja odtwarzania ścieżki
def odtworz_sciezke(mapa, rodzice, cel):
    obecny = cel
    sciezka = []
    while obecny:
        mapa[obecny[0]][obecny[1]] = 3  # 3 oznacza ścieżkę
        sciezka.append(obecny)
        obecny = rodzice[obecny]
    return sciezka[::-1]  # Odwracamy bi 0,0 jest na dole z niewiadomych mi przyczyn

# Sprawdzenie poprawności
def czy_valid(mapa, p):
    return 0 <= p[0] < len(mapa) and 0 <= p[1] < len(mapa[0]) and mapa[p[0]][p[1]] != 5

# Funkcja do wyświetlania mapy z kolorowaniem cyfr (tu sie dzieje magia coloramy)
def wyswietl_mape(mapa, koszt=None):
    for rzad in mapa:
        for pole in rzad:
            if pole == 5:
                print(Fore.RED + str(pole), end=' ')
            elif pole == 3:
                print(Fore.GREEN + str(pole), end=' ')
            else:
                print(str(pole), end=' ')
        print()

    if koszt is not None:
        print(Fore.CYAN + f"Koszt całkowity: {koszt}")

# wczytujemy wszystko co potrzebne
mapa = wczytaj_mape('grid.txt')
START = (len(mapa) - 1, 0)
CEL = (0, len(mapa[0]) - 1)

sciezka, koszt = a_star(mapa, START, CEL)

if sciezka:
    wyswietl_mape(mapa)  # Wyświetlamy mapę ze scieżką benc
    print(Fore.YELLOW + "Ścieżka: ", sciezka)
    print(Fore.YELLOW + f"Koszt przejścia w jedną stronę: {koszt}")

    # Koszt w obie strony (dodanie kosztu startowego i końcowego)
    calkowity_koszt = koszt + (len(mapa) - 1) + (len(mapa[0]) - 1)
    print(Fore.YELLOW + f"Koszt w obie strony: {calkowity_koszt}")
else:
    print(Fore.RED + "Brak ścieżki!")
