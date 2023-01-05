PROJEKT Z UUI
=============

Tvorba modelu
--------------
* V prvom kole sme použili sieť, ktorá mala 1 skrytú vrstvu a na nej 16 neurónov
* Chceli sme na nej zistiť najlepšiu kombináciu aktivačných funkcií
* Ako aktivačné funkcie sme skúšali hyperbolický tangens, sigmoidovú funkciu, ReLU a nakoniec lineárnu funkciu
* Testovali sme tak, že vyskúšali každú funkciu na každej vrstve a vypočítali sme si výslednú chybu ako 0.3train_error + 0.7test_error a následne sme si vybrali najlepších kandidátov.
* Trénovanie modelu prebiehalo v 50 epochách
* Náhodné hodnoty sme genrovali z rozdelenia N(0, 1/3)
* rýchlosť učenia alpha bola 0.1
* Výsledné honoty boli nasledovné:

f1, f2         | train_error | test_error | total_error
---------------|-------------|------------|------------
sigmoid, relu  |0.81829483   |0.22230778  |0.4011039
sigmoid, tanh  |0.37733077   |0.10222123  |0.18475409
sigmoid, linear|0.33415336   |0.09193737  |0.16460217
relu, sigmoid  |0.63317761   |0.1729111   |0.31099106
relu, tanh     |0.51537092   |0.15295337  |0.26167863
relu, linear   |0.551217220  |0.15441661  |0.27345679
tanh, sigmoid  |0.62685663   |0.17302799  |0.30917658
tanh, relu     |0.81829483   |0.22230778  |0.4011039
tanh, linear   |0.36629134   |0.1021441   |0.18138827
linear, sigmoid|0.9927434    |0.27207988  |0.48827894
linear, relu   |0.81829483   |0.22230778  |0.4011039
linear, tanh   |0.79554702   |0.21604676  |0.38989684

* Ale keďže výsledné hodnoty nie sú z intervalu [0, 1], na výslednej vrstve sme sa rozhodli použiť
lineárnu funkciu x + 1 (+1 preto, lebo výsledné hodnoty viac zasahujú do kladných hodnôt ako záporných)
* Následne sme odskúšali modely, ktoré mali na výslednej vrstve lineárnu aktivačnú funkciu a otestovalie sme
zvyšné 3 aktivačné funkcie na skrytej vrstve, aby sme zistili, ktorá bude najvhodnejšou
* Počet učiacich sa epoch sme natavili teraz na 100 a alphu sme nechali rovnakú
* Výsledné errory, ktoré sme dostali sú:

fcia   | train_error | test_error | total_error
-------|-------------|------------|------------
sigmoid|0.45788102   |0.12326298  |0.22364839
tanh   |0.43101548   |0.11254077  |0.20808318
relu   |0.61450503   |0.16092987  |0.29700242

* Preto sme sa rozhodli na skrytých vrstvách používať hyperbolický tangens

Zisťovanie počtu skrytých neurónov
---------------
* Keď už sme mali vybrané aktivačné funkcie, v ďalšom kroku sme chceli zistiť, aký počet neurónov je optimálny
* Na testovanie sme opäť použili dvojvrstvovú sieť s rýchlosťou učenia 0.1
* Aktivačná funkcia na skrytej vrstve bola tanh a na vonkajšej bola lineárna
* Skúšali sme počty neurónov 8, 10, 12 ... 50
* Výsledné errory sú zhrnuté v nasledovnej tabuľke:

počet neurónov | total error
---------------|------------
8              |0.34141076
10             |0.49546223
12             |0.43364913
14             |0.30725816
16             |0.42649649
18             |0.3175108
20             |0.43872581
22             |0.35504076
24             |0.3953254
26             |0.58908309
28             |0.29286061
30             |0.3819434
32             |0.35375606
34             |0.47723399
36             |0.36689453
38             |0.28084964
40             |0.27341348
42             |0.31580463
44             |0.30428932
46             |0.36510255
48             |0.37062686
50             |0.34816912