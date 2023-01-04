PROJEKT Z UUI
=============

Tvorba modelu
--------------
* V prvom kole sme použili sieť, ktorá mala 1 skrytú vrstvu a na nej 16 neurónov
* Chceli sme na nej zistiť najlepšiu kombináciu aktivačných funkcií
* Ako aktivačné funkcie sme skúšali hyperbolický tangens, sigmoidovú funkciu, ReLU a nakoniec lineárnu funkciu
* Testovali sme tak, že vyskúšali každú funkciu na každej vrstve a vypočítali sme si výslednú chybu ako 0.3train_error + 0.7test_error a následne sme si vybrali najlepších kandidátov.
* Výsledné honoty boli nasledovné:

f1, f2       | train_error | test_error | total_error
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

