# Realtime Sales analytics

## Introduction

Le script Java `DataStreamJob.java` est un programme Flink qui utilise Apache Flink pour traiter en temps réel les
données provenant d'un topic Kafka. Les données sont des transactions de ventes représentées par la classe Order. Les
résultats sont stockés dans une base de données PostgreSQL, avec des tables telles que transactions, sales_per_category,
sales_per_day, et sales_per_month.

## Flux de Données en Temps Réel avec Apache Flink et Kafka

Le module **ecom** de ce projet utilise Apache Flink pour traiter les données en temps réel provenant du topic Kafka `
product_sold`.

Les transactions sont agrégées et mises à jour en continu dans la base de données PostgreSQL. Cette approche permet
d'avoir des informations en temps réel sur les ventes et les catégories de produits.

## Dépendances

- Apache Flink: Framework de traitement de données en temps réel.
- Apache Kafka: Plateforme de streaming distribuée.
- PostgreSQL JDBC Driver: Pilote JDBC pour la connexion à PostgreSQL.

## Configuration

Avant de compiler et exécuter le programme, assurez-vous de configurer les informations suivantes dans le
fichier `DataStreamJob.java` :

- URL JDBC pour la base de données PostgreSQL (`jdbcUrl`)
- Identifiants de connexion PostgreSQL (`username`, `password`)
- Les détails de la source Kafka (bootstrap servers, topic, group id)

## Source de Données Kafka

Utilise la source Kafka pour lire les données du topic "product_sold". Utilise un désérialiseur JSON personnalisé (
JSONDeserializer) pour convertir les messages Kafka en objets Order.

## Traitement et Stockage des Données

Crée une instance de KafkaSource pour lire les données Kafka. Applique des transformations sur le DataStream<Order>
pour agréger et traiter les données. Utilise le sink JDBC (JdbcSink) pour créer et mettre à jour les tables PostgreSQL.

## Création des Tables

Utilise le sink JDBC pour créer les tables PostgreSQL telles que transactions, sales_per_category, sales_per_day, et
sales_per_month.

## Insertion et Mise à Jour des Données

Utilise le sink JDBC pour insérer et mettre à jour les données dans les tables PostgreSQL. Les requêtes SQL
d'insertion/mise à jour sont définies dans le code.

## Mise à Jour des Ventes par Catégorie, Jour et Mois

Agrège les données pour mettre à jour les tables sales_per_category, sales_per_day, et sales_per_month à partir des
transactions brutes.

## Compilation du Projet

1. Assurez-vous que vous avez Apache Flink et Apache Kafka installés et configurés correctement.
2. Compilez le projet en utilisant un gestionnaire de construction Maven.

```bash
mvn clean package
```

Cela génèrera un fichier jar `ecom-1.0.jar` que l'on soumettra à Flink soit avec son interface soit par code

## Soumission du Job Flink

Assurez-vous que votre cluster Flink est en cours d'exécution. Utilisez la commande flink run pour soumettre le job en
utilisant le fichier JAR généré.

```bash
./bin/flink run -c DataStreamJob target/ecom-1.0.jar
```

Surveillez la sortie pour vérifier que le job est en cours d'exécution sans erreurs.

## Notes Supplémentaires

    Assurez-vous que les dépendances nécessaires (Flink, Kafka, etc.) sont correctement installées et configurées.
    Les requêtes SQL utilisées dans le code sont adaptées au dialecte PostgreSQL. Veuillez les ajuster si vous utilisez une autre base de données.

## Contributions

Les contributions sont les bienvenues ! Si vous avez des idées d'améliorations, veuillez ouvrir une issue ou soumettre
une demande de fusion.

## Auteurs

    Nom : Mohamed DIALLO
    email : mohameddiallo728@gmail.com

## Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](https://opensource.org/licenses/MIT) pour plus de détails.

La licence MIT est une licence open source permissive qui permet une utilisation, modification, et distribution libre du
code source. Elle est souvent utilisée pour les projets open source, car elle offre une grande liberté aux utilisateurs
tout en protégeant les droits d'auteur et la responsabilité de l'auteur du code.

[Lire la licence MIT](https://opensource.org/licenses/MIT)
