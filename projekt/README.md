PROJEKT Z UUI
=============

Tvorba modelu
--------------
* V prvom kole sme použili sieť, ktorá mala 1 skrytú vrstvu a na nej 16 neurónov
* Chceli sme na nej zistiť najlepšiu kombináciu aktivačných funkcií
* Ako aktivačné funkcie sme skúšali hyperbolický tangens, sigmoidovú funkciu, ReLU a nakoniec lineárnu funkciu
* Testovali sme tak, že vyskúšali každú funkciu na každej vrstve a vypočítali sme si výslednú chybu ako 0.3train_error + 0.7test_error a následne sme si vybrali najlepších kandidátov.
* Výsledné honoty boli nasledovné:
(f1, f2)       | train_error | test_error | total_error
---------------|-------------|------------|------------
sigmoid, relu
sigmoid, tanh
sigmoid, linear
relu, sigmoid
relu, tanh
relu, linear
tanh, sigmoid
tanh, relu
tanh, linear

