# Programació per a la ciència de dades - PAC4

Autor: Albert Salvador

Última modificació: 11/06/2022

També disponible a: https://github.com/ASYuste/pcd_pac4

## Context

Treballeu per a una empresa que crea solucions “Data Science” per a projectes de tot tipus. L'equip directiu vol centrar-se en els propers anys en el món dels e-sports, de ràpid creixement, i ha decidit començar amb un que no els resultat una mica més conegut, el FIFA.
Ens han demanat que dissenyem eines per treballar amb aquest tipus de dades, tant en termes d'anàlisi exploratòria de dades com a llarg termini. Per això, ens han proporcionat un conjunt de dades que inclou tota la informació sobre els jugadors i les jugadores del videojoc entre els anys 2016 i 2022.

## Contingut

Aquest programa contempla resoldre totes aquelles consultes generades al llarg de la PAC4 de l'assignatura de Programació per a la ciència de dades de la UOC (Curs 2021/22). Aquesta PAC es divideix en 6 exercicis.

- L'exercici 1 consisteix en la creació d'unes funcions que permetran llegir uns arxius de jugadors i jugadores del videojoc FIFA, contingudes a la carpeta `data`, cadascun amb condicions i requirements diferents.
- L'exercici 2 cerca obtenir certes estadístiques bàsiques del conjunt de futbolistes amb la creació d'unes funcions, tot aplicant filtres adequats. A l'últim apartat d'aquest exercici se'ns presenta un problema concret.
- L'exercici 3 calcula l'índex de massa corporal (BMI) de cada jugador i el compara amb la població general. Es generen resultats per pantalla i en forma de gràfics. Es comenten algunes observacions dels resultats als comentaris del mateix programa.
- L'exercici 4 vol aconseguir l'evolució dels jugadors enfront alguna variable amb el pas del temps. Per a tal fi es defineixen unes funcions de creació i neteja de diccionaris amb les dades dels jugadors d'interès.
- A l'exercici 5, tot utilitzant les funcions anteriors i una nova en què es calculen els millors jugadors en una categoria, se'n representa una evolució dels millors jugadors en la categoria especificada.
- Finalment l'exercici 6 aborda una proposta de cas real. En aquest es proposa crear una línia de defensa per un equip masculí, femení i un de mixte veterà (>30 anys). Sobre múltiples combinacions de línies de defensa enfront a unes característiques destacades, es presenten totes les alineacions per la puntuació general obtinguda, així com valors d'atac, defensa i possessió.

## Utilitzant el programa

### Format d'entrada

El programa està contingut en un sol script `main.py`. En ell s'hi contenen totes les funcions creades demanades per els exercicis 1-5. A més, s'hi inclouen un parell de funcions addicionals utilitzades per a l'exercici 6.

Quan es realitzi la crida del programa s'aniran executant tots els exercicis de la pràctica, un rere l'altre, retornant per pantalla els resultats esperats.

### Passos per executar main.py

1. `pip install -r requirements.txt`
2. `python3 main.py`

El programa no contempla més paràmetres per línia de comandes, doncs està automatitzat de manera que s'executi automàticament amb els paràmetres indicats a la pràctica

### Sortida de programa

El programa presenta per pantalla els resultats que es demanen. Addicionalment es generen alguns gràfics que, alhora que es mostren per pantalla, es guarden a la carpeta `result`.

## Testant el programa

### Test_public i Test_custom

Es vol comprovar que el programa `main.py` resolgui adecuadament totes les necessitats que se'n depenguin d'ell. D'aquesta manera se'l sotmet a dos tests, un proposat pel professorat (`test_public.py`) i un d'intern generat adhoc (`test_custom.py`), per comprovar que el resultat és l'esperat. Aquests tests es poden observar a la carpeta `tests`.

### Passos per testar el programa

En cas de no tenir instal·lat `HTMLTestRunner` instalar amb la següent comanda:

1. `pip install HTMLTestRunner-rv`

Passar el test public:

2. `python3 -m tests.test_public`

Passar el test intern:

3. `python3 -m tests.test_custom`

### Sortida

S'espera una sortida conforme cada test ha sigut passat satisfactòriament. Aquest vindrà marcat per un `ok` al inici de cada sortida, de la forma següent:

`ok test_custom_1 (__main__.CustomTestsEx2)`