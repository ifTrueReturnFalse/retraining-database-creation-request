# Projet 6 OC – Créez et utilisez une base de données immobilières / Project 6 OC – Create and Use a Real Estate Database

[![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff)](#)
[![SQLite](https://img.shields.io/badge/SQLite-%2307405e.svg?logo=sqlite&logoColor=white)](#)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-blue)

---

## 🇫🇷 Version française

Ceci est le dépôt GitHub d’un projet réalisé dans le cadre de ma formation **Développeur IA** avec OpenClassrooms.

L’objectif principal est de concevoir une **base de données immobilières** et de créer des requêtes afin d'exploiter celle-ci pour mieux étudier le marché. 
Le contexte de ce projet est de le réaliser au sein d'un groupe d'agences immobilières afin de créer des outils futurs pour aider les agents dans leurs estimations et recherches. 

La base de données a été conçue après l'analyse des données sources fournies au format Excel, pour être adaptée sous **SQLite**.
Elle respecte la norme **3NF** et les règles de **RGPD** afin de garantir confidentialité et performance.

### Fonctionnalités Clés

- Création de la base de données.
- Implémentation de la structure de la base de données en **Python** (via **SQLAlchemy** et **Alembic**).
- Script d'injection de données optimisé (via **Pandas**) pour peupler la base rapidement.
- Création de requêtes SQL pour l'exploitation de la base.

## Technologies utilisées

| Pile Technique                | Outil               | Rôle                                                                |
| :---------------------------- | :------------------ | :------------------------------------------------------------------ |
| **Manipulation des données** | **Pandas** | Librairie de manipulation des données afin de fournir les bonnes données à injecter dans la base de données. |
| **Moteur de base de données**        | **SQLite**         | Base de données légère parfaite pour un fonctionnement en local et du prototypage.          |
| **Manipulation de base de données** | **SQLAlchemy** | Permet de manipuler facilement la base de données grâce au langage Python. |
| **Gestion de version**          | **Alembic**     | Solution de gestion de version de base de données. |
| **Exploitation de la base**         | **SQL**        | Langage le plus courant pour faire des requêtes sur les bases de données. |

## Installation & utilisation

> J'ai utilisé [Poetry](https://python-poetry.org/docs/) pour gérer mes dépendances, il est préférable que vous l'ailliez également sur votre machine pour installer au mieux ce projet.

1. Cloner le dépôt

```bash
git clone https://github.com/ifTrueReturnFalse/retraining-database-creation-request.git
cd retraining-database-creation-request
```

2. Installer les dépendances

```bash
poetry install
```

3. Créer la base de données

```bash
poetry run alembic upgrade head
```

<details>
  <summary><b>Alternative : Création manuelle</b></summary>

  Toutes les requêtes SQL pour créer les tables manuellement sont présentent dans le fichier : [requetes_creation.md](./requetes_creation.md).
</details>

4. Injecter les données dans la base de données

```bash
poetry run python populate.py
```

5. Faire des requêtes SQL

Une douzaine de requêtes demandées lors du projets sont présentes et documentées dans le fichier [requetes.md](./requetes.md)

<details>
  <summary><b>Exemple :</b> Les moyennes de valeurs foncières pour le top 3 des communes des départements 6, 13, 33, 59 et 69, classées par moyenne foncière</summary>
  
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

</details>

Sinon vous pouvez utiliser n'importe quel logiciel permettant d'intéragir avec une base de données SQLite pour faire des requêtes. 

Dans mon cas j'ai utilisé [SQLite Studio](https://sqlitestudio.pl/) et [DBeaver](https://dbeaver.io/) lors de la réalisation de ce projet. 

---

## 🇬🇧 English version

This is a GitHub repository for a project completed as part of my **AI Developer** training program with OpenClassrooms.

The main goal is to design a **real estate database** and create SQL queries to exploit the data for better market analysis.  
The context of this project is to implement it within a group of real estate agencies to build future tools that will assist agents in their valuations and searches. 

The database schema was designed after analyzing the source data provided in Excel format, and was adapted for use with **SQLite**.  
It adheres to the **3NF** standard and **GDPR** rules to ensure confidentiality and optimal performance.

### Key Features

- Database schema creation.
- Implementation of the database structure in **Python** (using **SQLAlchemy** and **Alembic**).
- Optimized data injection script (using **Pandas**) to quickly populate the database.
- Creation of **SQL** queries for data exploitation and analysis.

## Technologies Used

| Technical Stack               | Tool              | Role                                                                |
| :---------------------------- | :------------------ | :------------------------------------------------------------------ |
| **Data Manipulation** | **Pandas** | Python library for data manipulation, ensuring the correct data is prepared for injection into the database. |
| **Database Engine**        | **SQLite**         | A lightweight database, perfect for local operation and prototyping.         |
| **Database Management** | **SQLAlchemy** | Allows easy manipulation of the database using the Python language. |
| **Version Control**          | **Alembic**     | A database migration and version control solution. |
| **Data Exploitation**         | **SQL**        | The most common language for querying databases. |

## Installation & Usage

> I used [Poetry](https://python-poetry.org/docs/) to manage dependencies. It is highly recommended that you also have it installed on your machine for the best project setup experience.

1. Clone the repository

```bash
git clone https://github.com/ifTrueReturnFalse/retraining-database-creation-request.git
cd retraining-database-creation-request
```

2. Install dependencies

```bash
poetry install
```

3. Create the database

```bash
poetry run alembic upgrade head
```

<details>
  <summary><b>Alternative: Manual Creation</b></summary>

  All the SQL queries needed to manually create the tables are available in the file: [requetes_creation.md](./requetes_creation.md).
</details>

4. Inject data into the database

```bash
poetry run python populate.py
```

5. Run SQL queries

A dozen queries requested during the project are available and documented in the file [requetes.md](./requetes.md)

<details>
  <summary><b>Example:</b> Average property values for the top 3 municipalities in departments 6, 13, 33, 59, and 69, ranked by average value</summary>
  
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

</details>

Alternatively, you can use any software that allows interaction with a SQLite database to run queries.

For this project, I personally used [SQLite Studio](https://sqlitestudio.pl/) and [DBeaver](https://dbeaver.io/).
