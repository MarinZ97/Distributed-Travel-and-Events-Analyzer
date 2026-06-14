# Distributed Travel and Events Analyzer

## Opis projekta

Ovaj projekt je napravljen za kolegij **Raspodijeljeni sustavi**.

Cilj projekta je omogućiti korisniku da unese **odredišni grad**, **grad polaska** i **vremenski period**, nakon čega sustav:
- dohvaća događaje preko **Ticketmaster API-ja**
- analizira moguće opcije **letova**
- analizira moguće opcije **smještaja**

Rezultat se prikazuje kroz web sučelje u obliku pregleda putovanja.

---

## Korištene tehnologije

U projektu su korištene sljedeće tehnologije:

- **FastAPI** – backend API
- **Redis** – broker poruka
- **Celery** – pozadinska/asinkrona obrada zadataka
- **Nginx** – reverse proxy i posluživanje frontenda
- **Docker Compose** – pokretanje i povezivanje svih servisa
- **Polars** – obrada CSV datasetova
- **HTML / CSS / JavaScript** – frontend

---

## Kako projekt radi

Korisnik preko frontenda unosi:
- destination city
- departure city
- date from
- date to
- način sortiranja letova
- način sortiranja smještaja

Nakon toga frontend šalje zahtjev prema API-ju.

API kreira novi posao i vraća `job_id`, a obrada se dalje izvodi u pozadini preko **Celery workera**.

Worker:
1. dohvaća evente preko Ticketmaster API-ja
2. analizira flights dataset
3. analizira accommodations dataset
4. vraća završeni rezultat

Frontend zatim provjerava status posla i na kraju prikazuje rezultat korisniku.

---

## Arhitektura sustava

Projekt se sastoji od nekoliko odvojenih dijelova:

- **frontend** – korisničko sučelje
- **api** – prima zahtjeve korisnika
- **worker** – obrađuje podatke u pozadini
- **redis** – koristi se kao message broker
- **nginx** – služi frontend i prosljeđuje API pozive

Sve komponente se pokreću preko `docker compose`.

---

## Izvori podataka

### 1. Ticketmaster API
Koristi se za dohvat događaja prema gradu i vremenskom periodu.

### 2. Kaggle flights dataset
Koristi se za analizu flight opcija.

### 3. Kaggle accommodations dataset
Koristi se za analizu smještaja.

---

## Napomena o podacima

Važno je napomenuti da u ovoj verziji projekta:

- **eventi** ovise o stvarnom API pozivu i vremenskom periodu
- **flights** i **accommodations** dolaze iz datasetova i služe kao analitičke opcije

Projekt nije potpuni booking sustav, nego demonstracija povezivanja više izvora podataka u jednu distribuiranu aplikaciju.

Kod flights dijela koristi se filtriranje po:
- destination city
- departure city
- sortiranju (cheapest / expensive)

Kod accommodations dijela koristi se sortiranje po:
- cheapest
- expensive
- best rating

---

## Preduvjeti

Za pokretanje projekta potrebno je imati instalirano:

- Docker
- Docker Compose
- Ticketmaster API key

---

## Pokretanje projekta

Nakon pokretanja aplikacija je dostupna na:

`http://localhost:8080`

Projekt se pokreće iz root foldera naredbom:

```bash
docker compose up --build -d