# Sars-CoV-2-Challenge
Pràctica d'Algorítmica i Complexitat  
### Preprocessament:
#### Càlcul de medianes:
- Hem descarregat la informació en csv de totes les seqüències, ordenades per llargada ("all_sequences.csv").
- Hem filtrat les dades per país, sense diferenciar les regions.
- Hem calculat la mediana accedint a la posició directament, ja que les dades ja estaven ordenades.  
- Hem accedit a la mostra i l'hem descarregat en format FASTA.
#### Alineament de seqüències
##### Força bruta
- Hem generat tots els alineaments possibles, per després mirar quina és la millor.
##### Mètode Needleman-Wunsch
- Aplicant programació dinàmica, hem creat una taula que ens permet resseguir el camí per alinear les seqüències (traceback matrix).
- També hem creat una taula que ens permet puntuar la similitud entre les dues seqüències
##### Mètode Needleman-Wunsch Optimitzat
- És el mateix que el mètode anterior, però omplim la taula de forma recursiva.
