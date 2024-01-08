# Générateur de Transactions de Vente Simulées

## Aperçu

Ce script Python génère des transactions de vente simulées et les produit dans un topic Kafka nommé `product_sold`.

Les transactions incluent des informations telles que les détails du produit, les détails du client, la date de commande
et le mode de paiement.

## Dépendances

- confluent_kafka
- Faker

Assurez-vous d'avoir installé ces dépendances avant d'exécuter le script.

## Utilisation

1. Installer les dépendances : `pip install confluent_kafka` et `pip install Faker`
2. Exécuter le script : `python main.py`

## Configuration

- Serveurs d'amorçage Kafka : `localhost:9092`
- Topic Kafka : `product_sold`

## Sortie

Le script produit des transactions de vente simulées et les imprime dans la console. Le statut de livraison de chaque
message est également affiché.

## Notes

- Le script s'exécute pendant 120 secondes, générant et envoyant des transactions de vente toutes les 2 secondes.
- Si le tampon du producteur Kafka est plein, il attend une seconde avant de tenter à nouveau l'envoi du message.

## Explication globale

### 1. Génération de Données :

`simple_profile` : Utilise le module fake pour générer un profil utilisateur fictif.

`order_date` : Génère une date de commande aléatoire dans la décennie en cours et ajoute un nombre aléatoire de jours.

`category` : Sélectionne de manière aléatoire une catégorie de produit parmi des catégories prédéfinies.

`product_info` : Sélectionne de manière aléatoire un nom et une marque de produit en fonction de la catégorie choisie.
Génère un prix, une quantité et une devise aléatoires. Ajuste le prix si la devise est FCFA.

`Détails de la Transaction` : Construit un objet JSON représentant une transaction de vente simulée, comprenant l'ID de
commande, l'ID de produit, l'ID de client et d'autres détails pertinents.

### 2. Boucle de Génération de Ventes

Une boucle génère et envoie des transactions de vente simulées à Kafka :

    Durée de la Boucle : La boucle s'exécute pendant 120 secondes.
    Gestion du Tampon : Si le tampon du producteur Kafka est plein, il attend une seconde avant de tenter à nouveau l'envoi du message.
    Compteur Total de Ventes : Compte le nombre total de transactions de vente générées.

### 3. Production de Messages Kafka

Pour chaque itération, le script :

    Appelle la fonction generate_sales pour créer une transaction de vente simulée.
    Utilise le producteur Kafka pour envoyer la transaction au topic 'product_sold'.
    Imprime la transaction de vente générée à des fins de débogage.
    Attend 2 secondes avant d'envoyer la prochaine transaction.

### 4. Rapport de Livraison Callback

La fonction delivery_report est un rappel qui imprime un message indiquant si la livraison du message a réussi ou
échoué.

### 5. Fonction Principale

La fonction main initialise le producteur Kafka, lance la boucle de génération de ventes et imprime le nombre total de
transactions de vente générées.

### 6. Exécution du Script

Pour exécuter le script, exécutez-le directement (python main.py). 

Assurez-vous que les dépendances requises sont installées et que Kafka fonctionne sur `localhost:9092`.

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



