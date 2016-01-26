# Doooooominus
- Mini-Rapport
- Autheurs: Romain Claret & Nils Ryter

# Table des matières

Introduction	3
- Avis personnel	3
- Mon approche du projet	3
Objectif	4
- Accompli	4
- Inaccompli	4
Apprentissage	5

# Rapport Technique

## Contexte

C'est dans le cadre du projet de compilateur que nous avons réalisé ce langage merveilleux dont plus d'un romains serait jaloux : Doooooominus !

## But

Réaliser un compilateur qui reçoive un code écrit en latin et qui le compile en python.
A la base, nous pensions compiler pour une machine de turing ou une machine brainfuck, mais la distance entre notre langage latin et ceux-ci aurait rendue le projet trop complexe.
Nous avons donc choisi de changer notre cible et de prendre n'importe quelle machine capable de faire tourner un interpréteur python.

## Fonctionnalités
Notre programme prend en charge les fonctions suivantes :

### Affectation

Il est possible de définir une variable avec la syntaxe suivante et/ou de lui affecter/réaffecter une nouvelle valeur :
- **est**: ASSIGN

### Structure conditionnelle

Le « if » des langage courant s'écrit « alterum ». La condition est terminer par un « then » qui s'écrit « ergo »

- **alterum**: IF
- **aut**: ELSE
- **ergo**: THEN
- **initium**: BEGIN
- **exitus**: END

### Structure itérative

- **facite**: DO
- **iterum**: WHILE
- **perfectus**: DONE

### Display
- **scriptor**: PRINT
  

### Arithmetic operators
- **multiplico**: TIMES
- **addo**: PLUS
- **minus**: MINUS
- **divide**: DIVIDE

### Logic operators
- **et**: AND
- **vel**: OR
- **xor**: XOR
- **non**: NOT
- **vera**: TRUE
- **falsa**: FALSE

### Relational operators
- **humilior**: LOWERTHEN
- **maior**: GREATERTHEN
- **idem**: EQUAL