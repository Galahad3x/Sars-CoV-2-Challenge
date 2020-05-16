# Sars-CoV-2-Challenge
Pràctica d'Algorítmica i Complexitat  
### Preprocessament:
#### Càlcul de medianes:
- Hem descarregat la informació en csv de totes les seqüències, ordenades per llargada ("all_sequences.csv").
- Hem filtrat les dades per país, sense diferenciar les regions.
- Hem calculat la mediana accedint a la posició directament, ja que les dades ja estaven ordenades.  
- Hem accedit a la mostra i l'hem descarregat en format FASTA.
#### Alineament de seqüències
- Sense RAM a partir de ~26000 caracters (25GB)
- Separar les seqüències no seria possible (error AAAC-AC)
##### Força bruta
- Hem generat tots els alineaments possibles, per després mirar quina és la millor. No és fiable si les mostres tenen la mateixa llargada, ja que no genera més alineacions.
##### Mètode Needleman-Wunsch
- Aplicant programació dinàmica, hem creat una taula que ens permet resseguir el camí per alinear les seqüències (traceback matrix).
- També hem creat una taula que ens permet puntuar la similitud entre les dues seqüències.
- L'algoritme té 2 versions, una per trobar la puntuació i l'alineament i una altra que només troba la puntuació.
##### Mètode Needleman-Wunsch Optimitzat
- És el mateix que el mètode anterior, però omplim la taula de forma recursiva. No ens és gaire útil, ja que a partir de pocs caràcters (més o menys 1000) salta l'error RecursionError: Maximum recursion depth exceeded.
#### Mètode de classificació
##### Hierarchical clustering
- Utilitzant una matriu de distàncies.
- Per fusionar dues matrius, fer la mitjana dels 2 elements.
