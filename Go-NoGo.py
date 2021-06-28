from psychopy import visual, core, event
import random
import csv

RESULTS = [["NUMBER", "EXPERIMENT", "TYPE", "CORRECT", "REACTION"]]


# funkcja czeka na naciśnięcie przycisku, jeśli ustawiony jest timeout i użytkownik nic nie nacisnął, funkcja zwraca None
def reactions(keys, timeout=None):
    event.clearEvents()
    if not timeout is None:
        key = event.waitKeys(keyList=keys, maxWait=timeout)
    else:
        key = event.waitKeys(keyList=keys)
    return key


# funkcja pokazuje tekst i uruchamia funkcję reactions
def show(win, info, wait_key=["return"], timeout=None):
    info.draw()
    win.flip()
    reactions(wait_key, timeout=timeout)


# główna funkcja eksperymentu
#
# n - liczba testów
# ex - eksperyment lub test
# disable_no_go - wyłacza no-go
def exp(n, ex=True, disable_no_go=False):
    for i in range(n):

        if disable_no_go:
            a = "go"

        else:
            if random.randint(1, 4) == 1:  # bierzemy losowo, jesli 1, to no-go
                a = "no-go"
            else:
                a = "go"

        j[a].draw()  # wyświetlenie tekstu
        window.callOnFlip(clock.reset)  # zresetowanie timera
        window.flip()  # zaktualizowanie obrazu

        r = reactions(["space"], 1.5)  # czekamy na naciśnięcie spacji lub 1,5 sekundy
        rt = clock.getTime()  # otrzymujemy czas
        window.flip()

        # przetworzamy wyniki, w razie potrzeby wyświetlia się tekst błędu
        if a == "go":
            et = "psh"
            if r is None:
                res = "0"
                show(window, error, timeout=1)
            else:
                res = "1"

        else:
            et = "pll"
            if not r is None:
                res = "0"
                show(window, error, timeout=1)
            else:
                res = "1"

        if ex:
            e = "trn"
        else:
            e = "exp"

        if r is None:
            rt = "x"

        RESULTS.append([i, e, et, res, rt])  # dodajemy wynik

        show(window, null, timeout=0.5)  # czekamy 0,5 sek


# ustawiamy timer
clock = core.Clock()

# uruchomiamy okno
window = visual.Window(units="pix", color="gray", fullscr=False)

# wyświetlamy wszystkie teksty
pull = visual.TextStim(win=window, text="PULL", height=20)
push = visual.TextStim(win=window, text="PUSH", height=20)
przerwa = visual.TextStim(win=window, text="PRZERWA", height=20)
error = visual.TextStim(win=window, text="ERROR", color=(255, 0, 0), colorSpace='rgb', height=20)
instr = visual.TextStim(win=window,
                        text="Dziękujemy za udział w badaniu. Twoim zadaniem będzie patrzenie na środek ekranu i reagowanie na bodźce. Jeśli zobaczysz PUSH, naciśnij SPACEBAR, jeśli zobaczysz PULL, zignoruj go. Napis “ERROR” będzie informował Cię o błędnej odpowiedzi lub braku odpowiedzi na poprzedni bodziec. W pewnym momencie będziesz miał(a) czas na odpoczynek, zobaczysz napis “PRZERWA”. Przerwę można przyśpieszyć przyciskiem ENTER. Najpierw będziesz miał(a) czas na trening, a potem zaczną się badania. Naciśnij ENTER, aby rozpocząć!",
                        height=20)
null = visual.TextStim(win=window, text=" ", height=20)

t1 = visual.TextStim(win=window, text="Trening 1 z 2", height=20)
t2 = visual.TextStim(win=window, text="Trening 2 z 2", height=20)
badanie = visual.TextStim(win=window, text="BADANIE", height=20)
dziekujemy = visual.TextStim(win=window, text="To już koniec! Dziękujemy za udział w badaniu 🙂", height=20)

j = {"go": push, "no-go": pull}

# pokazujemy narzędzia
show(window, instr)

# testowanie 1
show(window, t1)
exp(15, ex=False, disable_no_go=True)
show(window, przerwa)

# testowanie 2
show(window, t2)
exp(15, ex=False)
show(window, przerwa)

# eksperyment
show(window, badanie)
exp(50, ex=True)
show(window, przerwa)
exp(50, ex=True)
show(window, dziekujemy)

# zapisujemy wyniki
with open("result.csv", "w", newline='') as f:
    write = csv.writer(f)
    write.writerows(RESULTS)