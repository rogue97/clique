# Kurs: Računarska inteligencija

## Problem maksimalne klike (Maximum clique)
### Brute-force algortitam
Sa odsecanjem
```
src/brute_force.py
```

### Optimizacija genetskim algoritmom
```
src/genetski.py
```
Pokretanje na dva nacina iz terminala.


Prvi nacin:
```
naziv_fajla_koji_se_pokrece   broj_od_0_do_4_ili_nista
```
Ovim se pokrece genetski algoritam za 5 predefinisanih fajlova sa skupom cvorova i grana, preuzetih sa 
[DIMACS benschmark set](http://iridia.ulb.ac.be/~fmascia/maximum_clique)
index|naziv skupa| broj cvorova| broj grana grafa
-----|-----------|-------------|-----------------
0 | c125-9 | 125 | 6963
1 | brock200_4 | 200 | 13089
2 | gen400_p0-9_55 | 400  |71820
3 | p_hat300-3 | 300 | 33390
4 | DSJC1000-5 | 1000  |499652


Drugi nacin:
```
naziv_fajla_koji_se_pokrece   naziv_fajla_koji_se_ucitava   broj_iteracija
```

Izmeniti pocetne parametre fajla za dodatna testiranja.


Na svakoj od slika navedeno je od kog fajla sa skupom grana i cvorova je generisana maksimalna klika, kao i broj iteracija za koji se pokrenut program.


### NAPOMENA
- Grafici koji se generisu cuvaju se u folderu ciji je naziv naveden na pocetku fajla. Podrazumeva se da je folder kreiran. Ukoliko nije, slika nece biti sacuvana.

- Ne postoji cuvanje slika po timestamp-u tako da treba paziti ako se pokrene za razlicite parametre istog fajla sa podacima grafa a istim brojem iteracija(generacija).


