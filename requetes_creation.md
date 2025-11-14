```sql
-- 1. Table Region (aucune dépendance)
CREATE TABLE region (
    id_region INT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL
);
```

```sql
-- 2. Table Departement (dépend de Region)
CREATE TABLE departement (
    id_departement VARCHAR(3) PRIMARY KEY,
    id_region INT NOT NULL,
    nom VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_region) REFERENCES region(id_region)
);
```

```sql
-- 3. Table Commune (dépend de Departement)
CREATE TABLE commune (
    id_commune INT PRIMARY KEY,
    id_departement VARCHAR(3) NOT NULL,
    nom VARCHAR(50) NOT NULL,
    code_commune INT NOT NULL,
    code_insee VARCHAR(6) NOT NULL,
    population INT NOT NULL,
    FOREIGN KEY (id_departement) REFERENCES departement(id_departement)
);
```

```sql
-- 4. Table Bien (dépend de Commune)
CREATE TABLE bien (
    id_bien INT PRIMARY KEY,
    id_commune INT NOT NULL,
    btq VARCHAR(5),
    nombre_pieces INT NOT NULL,
    surface_carrez FLOAT NOT NULL,
    surface_local INT NOT NULL,
    type_bien VARCHAR(20) NOT NULL,
    FOREIGN KEY (id_commune) REFERENCES commune(id_commune)
);
```

```sql
-- 5. Table Vente (dépend de Bien)
CREATE TABLE vente (
    id_vente INT PRIMARY KEY,
    id_bien INT NOT NULL,
    date_vente DATE NOT NULL,
    valeur FLOAT NOT NULL,
    FOREIGN KEY (id_bien) REFERENCES bien(id_bien)
);
```