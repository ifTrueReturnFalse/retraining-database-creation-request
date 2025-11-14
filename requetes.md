# DATAImmo - POC

## Listes des requêtes SQL

### 1. Nombre total d’appartements vendus au 1er semestre 2020

```sql
SELECT
  COUNT(*) as nombre_ventes_appartements
FROM
  vente
INNER JOIN bien ON vente.id_bien = bien.id_bien
WHERE
  bien.type_bien = 'Appartement' AND
  strftime('%Y', vente.date_vente) = '2020' AND
  strftime('%m', vente.date_vente) <= '06'
```

_On peut théoriquement se passer de la condition sur les dates de vente car le jeu de données contient uniquement les ventes du premier semestre 2020._

Résultat
---

|nombre_ventes_appartements|
|-----|
|31374|

---

### 2. Le nombre de ventes d’appartement par région pour le 1er semestre 2020

```sql
SELECT
  region.nom as region,
  COUNT(*) as nombre_ventes_appartements
FROM
  vente
INNER JOIN bien ON vente.id_bien = bien.id_bien
INNER JOIN commune ON bien.id_commune = commune.id_commune
INNER JOIN departement ON commune.id_departement = departement.id_departement
INNER JOIN region ON departement.id_region = region.id_region
WHERE
  bien.type_bien = 'Appartement' AND
  strftime('%Y', vente.date_vente) = '2020' AND
  strftime('%m', vente.date_vente) <= '06'
GROUP BY region.nom
```

_On peut théoriquement se passer de la condition sur les dates de vente car le jeu de données contient uniquement les ventes du premier semestre 2020._

Résultat
---

|region|nombre_ventes_appartements|
|---|---|
|Auvergne-Rhône-Alpes|	3255|
|Bourgogne-Franche-Comté|	376|
|Bretagne|	983|
|Centre-Val de Loire|	695|
|Corse|	222|
|Grand Est|	984|
|Guadeloupe|	2|
|Guyane|	34|
|Hauts-de-France|	1252|
|Ile-de-France|	13995|
|La Réunion|	44|
|Martinique|	94|
|Normandie|	861|
|Nouvelle-Aquitaine|	1931|
|Occitanie|	1640|
|Pays de la Loire|	1357|
|Provence-Alpes-Côte d'Azur	|3649|

---

### 3. Proportion des ventes d’appartements par le nombre de pièces

```sql
WITH VentesParPieces AS (
  SELECT
    bien.nombre_pieces as nombre_pieces,
    COUNT(*) as nombre_ventes
  FROM
    vente
  INNER JOIN bien ON vente.id_bien = bien.id_bien
  WHERE
    bien.type_bien = 'Appartement'
  GROUP BY bien.nombre_pieces
)

SELECT
  nombre_pieces,
  nombre_ventes,
  ROUND( (nombre_ventes * 100.0 / NULLIF(SUM(nombre_ventes) OVER (), 0)), 3 ) AS proportion_pourcentage
FROM
  VentesParPieces
ORDER BY
  nombre_pieces
```

Explication de la requête :
- Récupération du nombre de ventes par nombre de pièces (aggrégation via `nombre_pieces`)
- Stockage de ce résultat dans une table temporaire `VentesParPieces`
- Création d'une deuxième table temporaire `CalculTotal`
- Cette table récupère le résultat de la table `VentesParPieces` et fait une somme des ventes grâce à `OVER`
- Les résultats sont ensuite mis en forme dans la requête finale afin d'obtenir le pourcentage de vente par nombre de pièces

_La division par zéro a été prise en compte dans le cas peu probable d'avoir aucune vente immobilière._

Résultat
---

|nombre_pieces|nombre_ventes|proportion_pourcentage|
|----|----|----|
|0|	30|	0.096|
|1|	6737	|21.477|
|2|	9776|	31.166|
|3|	8968|	28.59|
|4|	4457|	14.209|
|5|	1115|	3.555|
|6|	203|	0.647|
|7|	54|	0.172|
|8|	17|	0.054|
|9|	8|	0.026|
|10|	2	|0.006|
|11|	1|	0.003|

---

### 4. Liste des 10 départements où le prix du mètre carré est le plus élevé

```sql
SELECT
  departement.nom AS departement,
  ROUND(AVG(vente.valeur / NULLIF(bien.surface_carrez, 0)), 2) as prix_m2
FROM
  vente
INNER JOIN bien ON vente.id_bien = bien.id_bien
INNER JOIN commune ON bien.id_commune = commune.id_commune
INNER JOIN departement ON commune.id_departement = departement.id_departement
GROUP BY departement.nom
ORDER BY prix_m2 DESC
LIMIT 10
```

_Un arrondi a été effectué sur la moyenne du prix au m² pour être plus lisible._

_Une prévention sur la division par zéro est en place._

Résultat
---

|departement|prix_m2|
|---|---|
|Paris|	12053.48|
|Hauts-de-Seine|	7219.39|
|Val-de-Marne|	5341.59|
|Alpes-Maritimes|	4701.23|
|Haute-Savoie|	4667.13|
|Seine-Saint-Denis|	4344.78|
|Yvelines|	4225.25|
|Rhône|	4059.47|
|Corse-du-Sud|	4026.97|
|Gironde|	3760.92|

---

### 5. Prix moyen du mètre carré d’une maison en Île-de-France

```sql
SELECT
  ROUND(AVG(vente.valeur / NULLIF(bien.surface_carrez, 0)), 2) as prix_moyen_m2
FROM
  vente
INNER JOIN bien ON vente.id_bien = bien.id_bien
INNER JOIN commune ON bien.id_commune = commune.id_commune
INNER JOIN departement ON commune.id_departement = departement.id_departement
INNER JOIN region ON departement.id_region = region.id_region
WHERE 
  region.nom = 'Ile-de-France' AND
  bien.type_bien = 'Maison'
```

_Un arrondi a été effectué sur la moyenne du prix au m² pour être plus lisible._

Résultat
---

|prix_moyen_m2|
|----|
|3745.09|

---

### 6. Liste des 10 appartements les plus chers avec la région et le nombre de mètres carrés

```sql
SELECT
  region.nom AS region,
  bien.surface_carrez,
  vente.valeur
FROM
  vente
INNER JOIN bien ON vente.id_bien = bien.id_bien
INNER JOIN commune ON bien.id_commune = commune.id_commune
INNER JOIN departement ON commune.id_departement = departement.id_departement
INNER JOIN region ON departement.id_region = region.id_region
WHERE bien.type_bien = 'Appartement'
ORDER BY vente.valeur DESC
LIMIT 10
```

_Je suis bien dans ma campagne..._

Résultat
---

|region|surface_carrez|valeur|
|----|----|----|
|Ile-de-France	|9.1	|9000000.0|
|Ile-de-France|	64	|8600000|
|Ile-de-France	|20.55	|8577713|
|Ile-de-France|	42.77	|7620000|
|Ile-de-France	|253.3	|7600000|
|Ile-de-France	|139.9	|7535000|
|Ile-de-France	|360.95	|7420000|
|Ile-de-France	|595	|7200000|
|Ile-de-France	|122.56	|7050000|
|Ile-de-France	|79.38|	6600000|

---

### 7. Taux d’évolution du nombre de ventes entre le premier et le second trimestre de 2020

```sql
WITH VentesTrimestrielles AS (
  SELECT
    COUNT(CASE
      WHEN strftime('%m', vente.date_vente) IN ('01', '02', '03') 
      THEN 1
    END) AS ventes_t1,

    COUNT(CASE
      WHEN strftime('%m', vente.date_vente) IN ('04', '05', '06')
      THEN 1
    END) AS ventes_t2
    FROM
      vente
    WHERE
      strftime('%Y', vente.date_vente) = '2020' AND
      strftime('%m', vente.date_vente) <= '06'
)

SELECT
  ROUND((ventes_t2 - ventes_t1) * 100.0 / NULLIF(ventes_t1, 0), 2) as taux_evolution_ventes
FROM
  VentesTrimestrielles
```

Explication de la requête :
- Création d'une table temporaire `VentesTrimestrielles`, elle contiendra le nombre de ventes par trimestre
- Les `COUNT(CASE...WHEN...THEN...END)` permettent d'incrémenter les compteurs de ventes par trimestre en vérifiant si la date correspond
- Un `WHERE` est présent en amont afin de réduire le nombre d'itérations sur la table et augmenter les performances en production
- La requête finale permet de calculer l'évolution des ventes entre les deux premiers trimestres sous forme d'un pourcentage

_La division par zéro a été prise en compte dans le cas peu probable d'avoir aucune vente immobilière sur un trimestre._

Résultat
---

|taux_evolution_ventes|
|----|
|3.69|

---

### 8. Le classement des régions par rapport au prix au mètre carré des appartement de plus de 4 pièces

```sql
SELECT
  region.nom AS region,
  ROUND( AVG( vente.valeur / NULLIF(bien.surface_carrez, 0) ), 2 ) as prix_m2
FROM
  vente
INNER JOIN bien ON vente.id_bien = bien.id_bien
INNER JOIN commune ON bien.id_commune = commune.id_commune
INNER JOIN departement ON commune.id_departement = departement.id_departement
INNER JOIN region ON departement.id_region = region.id_region
WHERE 
  bien.type_bien = 'Appartement' AND
  bien.nombre_pieces > 4
GROUP BY region.nom
ORDER BY prix_m2 DESC
```

_La potentielle division par zéro a été anticipée dans le calcul du prix au m²._

Résultat
---

|region|prix_m2|
|----|----|
|Ile-de-France|	8759.3|
|La Réunion|	3641.81|
|Provence-Alpes-Côte d'Azur|	3587.65|
|Corse|	3104.88|
|Auvergne-Rhône-Alpes|	2891.38|
|Nouvelle-Aquitaine|	2465.48|
|Bretagne|	2412.05|
|Pays de la Loire|	2315.76|
|Hauts-de-France|	2189.93|
|Occitanie|	2097.23|
|Normandie|	2015.77|
|Grand Est|	1540.89|
|Centre-Val de Loire|	1453.11|
|Bourgogne-Franche-Comté|	1251.19|
|Martinique|	573.48|

---

### 9. Liste des communes ayant eu au moins 50 ventes au 1er trimestre

```sql
SELECT
  commune.nom AS commune,
  COUNT(*) AS nombre_ventes
FROM
  vente
INNER JOIN bien ON vente.id_bien = bien.id_bien
INNER JOIN commune ON bien.id_commune = commune.id_commune
WHERE 
  strftime('%m', vente.date_vente) IN ('01', '02', '03')
GROUP BY commune.id_commune, commune.nom
HAVING nombre_ventes >= 50
```

_L'aggrégation se fait sur l'id des communes pour éviter de regrouper des potentielles villes avec le même nom._

_Utilisation du_ `HAVING` _afin de filter sur les aggrégations._

Résultat
---

|commune|nombre_ventes|
|----|----|
|ANTIBES|	77|
|NICE|	173|
|CIOTAT (LA)|	62|
|MARSEILLE 1ER ARRONDISSEMENT|	71|
|MARSEILLE 4E  ARRONDISSEMENT|	72|
|MARSEILLE 8E  ARRONDISSEMENT|	81|
|MARSEILLE 9E  ARRONDISSEMENT|	66|
|NIMES	|63|
|TOULOUSE	|78|
|BORDEAUX|	157|
|SETE|	62|
|RENNES|	61|
|GRENOBLE|	106|
|NANTES|	119|
|ANGERS|	64|
|LILLE|	67|
|PARIS 2E  ARRONDISSEMENT|	61|
|PARIS 3E  ARRONDISSEMENT|	79|
|PARIS 4E  ARRONDISSEMENT|	59|
|PARIS 5E  ARRONDISSEMENT|	80|
|PARIS 6E  ARRONDISSEMENT|	86|
|PARIS 7E  ARRONDISSEMENT|	87|
|PARIS 8E  ARRONDISSEMENT|	62|
|PARIS 9E  ARRONDISSEMENT|	106|
|PARIS 10E  ARRONDISSEMENT|	109|
|PARIS 11E  ARRONDISSEMENT|	169|
|PARIS 12E  ARRONDISSEMENT|	110|
|PARIS 13E  ARRONDISSEMENT|	94|
|PARIS 14E  ARRONDISSEMENT|	146|
|PARIS 15E  ARRONDISSEMENT|	215|
|PARIS 16E  ARRONDISSEMENT|	165|
|PARIS 17E  ARRONDISSEMENT|	228|
|PARIS 18E  ARRONDISSEMENT|	209|
|PARIS 19E  ARRONDISSEMENT|	116|
|PARIS 20E  ARRONDISSEMENT|	127|
|VERSAILLES|	54|
|TOULON|	59|
|ASNIERES-SUR-SEINE|	81|
|BOULOGNE-BILLANCOURT|	99|
|COURBEVOIE|	80|
|ISSY-LES-MOULINEAUX|	50|
|LEVALLOIS-PERRET|	59|
|PUTEAUX|	53|
|RUEIL-MALMAISON|	68|
|MONTREUIL|	65|
|SAINT-MAUR-DES-FOSSES|	56|
|VINCENNES|	68|
|AJACCIO|	54|

---

### 10. Différence en pourcentage du prix au mètre carré entre un appartement de 2 pièces et un appartement de 3 pièces

```sql
WITH PrixMoyens AS (
  SELECT
    AVG(CASE
      WHEN bien.nombre_pieces = 2
      THEN (vente.valeur / NULLIF(bien.surface_carrez, 0))
    END) AS prix_moyen_2_pieces,
    
    AVG(CASE
      WHEN bien.nombre_pieces = 3
      THEN (vente.valeur / NULLIF(bien.surface_carrez, 0))
    END) AS prix_moyen_3_pieces
  FROM
    vente
  INNER JOIN bien ON vente.id_bien = bien.id_bien
  WHERE
    bien.type_bien = 'Appartement' AND
    bien.nombre_pieces IN (2, 3)
) 

SELECT
  ROUND( (prix_moyen_2_pieces - prix_moyen_3_pieces) * 100.0 / prix_moyen_3_pieces, 2) AS difference_2_3_pieces
FROM
  PrixMoyens
```

Explication de la requête :
- Création d'une table temporaire `PrixMoyens` qui contiendra le prix moyen au m² des appartements 2 et 3 pièces
- La moyenne se fait grace au `CASE` qui vérifie le nombre de pièces
- Un `WHERE` est fait en amont afin de réduire le nombre d'itérations dans les `CASE`
- La requête finale met juste en forme le résultat sous forme de pourcentage

Résultat
---

|difference_2_3_pieces|
|----|
|14.13|

---

### 11. Les moyennes de valeurs foncières pour le top 3 des communes des départements 6, 13, 33, 59 et 69

L'intitulé de la demande étant vague, j'ai réalisé plusieurs requêtes qui peuvent s'en rapprocher. 

Les 3 requêtes fonctionnent de manière similaire : 

- Création d'une table temporaire qui récupère les communes avec la valeur moyenne du foncier, sur les départements (6, 13, 33, 59, 69)
- La deuxième requête compte également le nombre de ventes, et la requête 3 récupère la population des communes
- Création d'une seconde table temporaire qui va mettre un rang par ville, partitionner par département en fonction de :
  - La moyenne de la valeur foncière pour la requête 1
  - Les ventes de bien pour la requête 2
  - La population par commune pour la requête 3
- Et ensuite la requête finale qui vient récupérer les rangs 1, 2 et 3 afin de les ranger par département puis par rang. 

#### Top 3 des communes par moyenne des valeurs foncières

```sql
WITH FoncierMoyenCommune AS (
  SELECT
    departement.id_departement as dep_id,
    commune.nom AS commune,
    ROUND(AVG( vente.valeur ), 2) AS moyenne_foncier
  FROM
    vente
  INNER JOIN bien ON vente.id_bien = bien.id_bien
  INNER JOIN commune ON bien.id_commune = commune.id_commune
  INNER JOIN departement ON commune.id_departement = departement.id_departement
  WHERE departement.id_departement IN (6, 13, 33, 59, 69)
  GROUP BY commune.id_commune, commune.nom
),

RangCommunes AS (
  SELECT
    dep_id,
    commune,
    moyenne_foncier,
    RANK() OVER (
      PARTITION BY dep_id
      ORDER BY moyenne_foncier DESC
    ) AS rang_valeur_fonciere
  FROM
    FoncierMoyenCommune
  )
  
SELECT
  departement.nom AS departement,
  commune,
  moyenne_foncier,
  rang_valeur_fonciere
FROM
  RangCommunes
INNER JOIN departement ON dep_id = departement.id_departement
WHERE rang_valeur_fonciere IN (1, 2, 3)
ORDER BY departement.nom ASC, rang_valeur_fonciere ASC
```

Résultat
---

|departement|commune|moyenne_foncier|rang_valeur_fonciere|
|----|----|----|----|
|Alpes-Maritimes|	SAINT-JEAN-CAP-FERRAT|	968750|	1|
|Alpes-Maritimes|	EZE|	655000|	2|
|Alpes-Maritimes|	MOUANS-SARTOUX|	476898.1|	3|
|Bouches-du-Rhône|	GIGNAC-LA-NERTHE|	330000|	1|
|Bouches-du-Rhône|	SAINT-SAVOURNIN|	314425|	2|
|Bouches-du-Rhône|	CASSIS|	313416.88|	3|
|Gironde|	LEGE-CAP-FERRET|	549500.64|	1|
|Gironde|	VAYRES|	335000|	2|
|Gironde|	ARCACHON|	307435.93|	3|
|Nord|	BERSEE|	433202|	1|
|Nord|	CYSOING|	408550|	2|
|Nord|	HALLUIN|	322250|	3|
|Rhône|	VILLE-SUR-JARNIOUX|	485300|	1|
|Rhône|	LYON 2E  ARRONDISSEMENT|	455217.27|	2|
|Rhône|	LYON 6E  ARRONDISSEMENT|	426968.25|	3|

#### Top 3 des communes par ventes foncières

```sql
WITH FoncierMoyenCommune AS (
  SELECT
    departement.id_departement as dep_id,
    commune.nom AS commune,
    ROUND(AVG( vente.valeur ), 2) AS moyenne_foncier,
    COUNT(*) AS nombre_ventes
  FROM
    vente
  INNER JOIN bien ON vente.id_bien = bien.id_bien
  INNER JOIN commune ON bien.id_commune = commune.id_commune
  INNER JOIN departement ON commune.id_departement = departement.id_departement
  WHERE departement.id_departement IN (6, 13, 33, 59, 69)
  GROUP BY commune.id_commune, commune.nom
),

RangCommunes AS (
  SELECT
    dep_id,
    commune,
    moyenne_foncier,
    RANK() OVER (
      PARTITION BY dep_id
      ORDER BY nombre_ventes DESC
     ) AS rang_ventes
  FROM
    FoncierMoyenCommune
  )
  
SELECT
  departement.nom AS departement,
  commune,
  moyenne_foncier,
  rang_ventes
FROM
  RangCommunes
INNER JOIN departement ON dep_id = departement.id_departement
WHERE rang_ventes IN (1, 2, 3)
ORDER BY departement.nom ASC, rang_ventes ASC
```

Résultat
---

|departement|commune|moyenne_foncier|rang_ventes|
|----|----|----|----|
|Alpes-Maritimes|	NICE|	273715.95|	1|
|Alpes-Maritimes|	ANTIBES|	256005.46|	2|
|Alpes-Maritimes|	MENTON|	208584.88|	3|
|Bouches-du-Rhône|	MARSEILLE 8E  ARRONDISSEMENT|	209837.13|	1|
|Bouches-du-Rhône|	MARSEILLE 4E  ARRONDISSEMENT|	115943.62|	2|
|Bouches-du-Rhône|	MARSEILLE 1ER ARRONDISSEMENT|	160203.93|	3|
|Gironde|	BORDEAUX|	253232.17|	1|
|Gironde|	MERIGNAC|	208139.92|	2|
|Gironde|	TALENCE|	183914.72|	3|
|Nord|	LILLE|	206779.14|	1|
|Nord|	ROUBAIX|	144011.81|	2|
|Nord|	VILLENEUVE-D'ASCQ|	141453.23|	3|
|Nord|	MADELEINE (LA)|	200915.94|	3|
|Nord| MARCQ-EN-BAROEUL|	188915.94|	3|
|Rhône|	VILLEURBANNE|	196082.8|	1|
|Rhône|	LYON 9E  ARRONDISSEMENT|	227282.6|	2|
|Rhône|	LYON 3E  ARRONDISSEMENT|	347104.21|	3|

#### Top 3 des communes par population

```sql
WITH FoncierMoyenCommune AS (
  SELECT
    departement.id_departement as dep_id,
    commune.nom AS commune,
    ROUND(AVG( vente.valeur ), 2) AS moyenne_foncier,
    commune.population AS population
  FROM
    vente
  INNER JOIN bien ON vente.id_bien = bien.id_bien
  INNER JOIN commune ON bien.id_commune = commune.id_commune
  INNER JOIN departement ON commune.id_departement = departement.id_departement
  WHERE departement.id_departement IN (6, 13, 33, 59, 69)
  GROUP BY commune.id_commune, commune.nom, commune.population
),

RangCommunes AS (
  SELECT
    dep_id,
    commune,
    moyenne_foncier,
    RANK() OVER (
      PARTITION BY dep_id
      ORDER BY population DESC
     ) AS rang_population
  FROM
    FoncierMoyenCommune
  )
  
SELECT
  departement.nom AS departement,
  commune,
  moyenne_foncier,
  rang_population
FROM
  RangCommunes
INNER JOIN departement ON dep_id = departement.id_departement
WHERE rang_population IN (1, 2, 3)
ORDER BY departement.nom ASC, rang_population ASC
```

Résultat
---

|departement|commune|moyenne_foncier|rang_population|
|----|----|----|----|
|Alpes-Maritimes|	NICE|	273715.95|	1|
|Alpes-Maritimes|	CANNES|	265021.37|	2|
|Alpes-Maritimes|	ANTIBES|	256005.46|	3|
|Bouches-du-Rhône|	AIX-EN-PROVENCE|	142000|	1|
|Bouches-du-Rhône|	MARSEILLE 13E  ARRONDISSEMENT|	151638.25|	2|
|Bouches-du-Rhône|	MARSEILLE 8E  ARRONDISSEMENT|	209837.13|	3|
|Gironde|	BORDEAUX|	253232.17|	1|
|Gironde|	MERIGNAC|	208139.92|	2|
|Gironde|	PESSAC|	182472.33|	3|
|Nord|	LILLE|	206779.14|	1|
|Nord|	TOURCOING|	115091.29|	2|
|Nord|	ROUBAIX|	144011.81|	3|
|Rhône|	VILLEURBANNE|	196082.8|	1|
|Rhône|	LYON 3E  ARRONDISSEMENT|	347104.21|	2|
|Rhône|	LYON 8E  ARRONDISSEMENT|	209562.1|	3|

---

### 12. Les 20 communes avec le plus de transactions pour 1000 habitants pour les communes qui dépassent les 10 000 habitants

```sql
WITH VenteParVille AS (
  SELECT
    commune.nom AS commune,
    commune.population AS population,
    COUNT(*) AS nombre_ventes
  FROM
    vente
  INNER JOIN bien ON vente.id_bien = bien.id_bien
  INNER JOIN commune ON bien.id_commune = commune.id_commune
  WHERE commune.population > 10000
  GROUP BY commune.id_commune, commune.nom, commune.population
)
  
SELECT
  commune,
  ROUND((nombre_ventes * 1000.0) / NULLIF(population, 0), 2) AS ventes_pour_1000
FROM
  VenteParVille
ORDER BY ventes_pour_1000 DESC
LIMIT 20
```

Résultat
---

|commune|ventes_pour_1000|
|----|----|
|PARIS 2E  ARRONDISSEMENT|	5.84|
|PARIS 1ER ARRONDISSEMENT|	4.86|
|PARIS 3E  ARRONDISSEMENT|	4.69|
|ARCACHON|	4.62|
|BAULE-ESCOUBLAC (LA)|	4.58|
|PARIS 4E  ARRONDISSEMENT|	4.05|
|ROQUEBRUNE-CAP-MARTIN|	3.99|
|PARIS 8E  ARRONDISSEMENT|	3.83|
|SANARY-SUR-MER|	3.5|
|PARIS 9E  ARRONDISSEMENT|	3.43|
|LONDE-LES-MAURES (LA)|	3.43|
|PARIS 6E  ARRONDISSEMENT|	3.38|
|SAINT-CYR-SUR-MER|	3.16|
|CHANTILLY|	3.13|
|PORNICHET|	3.06|
|SAINT-MANDE|	3.06|
|PARIS 10E  ARRONDISSEMENT|	3.04|
|MENTON|	2.94|
|SAINT-HILAIRE-DE-RIEZ|	2.87|
|VINCENNES|	2.81|