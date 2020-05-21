# Sars-CoV-2-Challenge
Pràctica d'Algorítmica i Complexitat  
### Fitxers per a l'execució:
- sarscovhierarcy.py <directory> -> Fitxer principal. De moment fa k-medoids clustering.
- setup.py <ruta all_sequences.csv> -> Executat com a sudo, crida als altres fitxers necessaris per a la mostra
- libraries.py -> Executat com a sudo, instala unes llibreries que necessitarem per a descarregar les mostres FASTA.
- fasta_finder.py -> Utilitza all_sequences.csv per a descarregar les mostres FASTA, i guarda el que ha tardat a time.txt.
- fasta_fixer.py -> Ens servirà per a substituïr nucleòtids que s'utilitzen com a abreviació. S'executa dins de fasta_finder.
- all_sequences.csv -> Dades sobre totes les seqüències en format CSV
- failsafe.py -> Executat amb python2.6 ens serveix com a guàrdia al provar els algoritmes. Si un algoritme està a punt de fer que l'ordenador es pengi, l'atura.
- map.html -> Resultat de k-medoids, representat gràficament.
### Preprocessament:
#### Càlcul de medianes:
- Hem descarregat la informació en csv de totes les seqüències, ordenades per llargada ("all_sequences.csv").
- Hem filtrat les dades per país, sense diferenciar les regions.
- Hem calculat la mediana accedint a la posició directament, ja que les dades ja estaven ordenades.  
- Hem accedit a la mostra i l'hem descarregat en format FASTA.
### Alineament de seqüències:
- Sense RAM a partir de ~26000 caracters (25GB)
- Separar les seqüències no seria possible (error AAAC-AC)
##### Força bruta: Python compilat i interpretat
- Hem generat tots els alineaments possibles, per després mirar quina és la millor. No és fiable, ja que tarda massa i gasta molta memòria.
##### Mètode Needleman-Wunsch: Python compilat i interpretat, Haskell i C
- Aplicant programació dinàmica, hem creat una taula que ens permet resseguir el camí per alinear les seqüències (traceback matrix).
- També hem creat una taula que ens permet puntuar la similitud entre les dues seqüències.
- L'algoritme té 2 versions, una per trobar la puntuació i l'alineament i una altra que només troba la puntuació.
##### Mètode Needleman-Wunsch Recursiu: Python compilat i interpretat
- És el mateix que el mètode anterior, però omplim la taula de forma recursiva. No ens és gaire útil, ja que a partir de pocs caràcters (més o menys 1000) salta l'error RecursionError: Maximum recursion depth exceeded.
##### Mètode Needleman-Wunsch Simple: Python compilat i interpretat, Haskell i C
- És el mètode Needleman-Wunsch iteratiu però, enlloc de generar la matriu completa solament genera una fila utilitzant l'anterior. No ens serveix per a trobar l'alineament de les seqüències, però si per a trobar la seva puntuació.
#### Mètode de classificació
##### Hierarchical clustering
- Utilitzant una matriu de distàncies.
- Per fusionar dues matrius, fer la mitjana dels 2 elements.
##### K-medoids:
- K-means pero tunejat
