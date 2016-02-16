# Doooooominus
- Projet de Compilateur
- Mini-Rapport
- Auteurs: Romain Claret \& Nils Ryter
- Abstract: Développement d'un interpréteur d'une langue inventée proche du latin en python.

# Table des matières
- Contexte....................................5
- But.............................................5
- Déroulement...............................5
- Fonctionnalités...........................5
	- Affectation..........................5
	- Structure conditionnelle.....6
	- Structure itérative..............6
	- Lecture...............................6
	- Structure arithmétique.......6
	- Structure relationnelle........7
	- Structure de priorité...........7
	- Structure du texte sacré....7
	- Les secrets de notre berger..8
- Exemple de prière d'amour.........8
- Exemple de prière finaboccienne...9

# Rapport technique

## Contexte

C'est dans le cadre du projet de compilateur que nous avons réalisé ce langage merveilleux dont plus d'un romain serait jaloux: Doooooominus!

## But

Notre objectif a été de réaliser un compilateur qui interprète un magnifique chant sacré écrit en latin et donne en résultat un texte en python profane.

## Déroulement
Au début, nous pensions compiler pour une machine de Turing ou une machine brainfuck, mais la distance entre notre langue sacrée en latin et ceux-ci aurait rendu le projet trop complexe.
Nous avons donc choisi de changer notre cible afin de pouvoir répandre la volonté de notre seigneur en interprétant nos chants sur n'importe quelle machine à l'aide de notre pierre de rosette, **python**.

## Fonctionnalités
Notre programme prend en charge les ordres sacrés suivants:

### Affectation

Il est effet possible de pouvoir définir une variable avec la syntaxe suivante et/ou de lui affecter/réaffecter une nouvelle valeur:

- **est**: assigner

### Structure conditionnelle

Dieu dans sa grande bonté nous a donné les conditions **if** des langages dits courants. La condition se termine par un **then** qui s'écrit **ergo**. Puis suit le bloc d'instruction encapsulé dans une clause **begin-end** qui se nome **initum-exitus**. L'alternative est possible avec le mot-clé **else**, sans oublier la clause **begin-end**. Merci, divin bienfaiteur.

- **alterum**: if
- **ergo**: then
- **initium**: begin
- **exitus**: end
- **aut**: else


### Structure itérative

C'est par la répétition que nous comprenons la volonté du puissant ! Pour répondre à sa demande, nous y avons donné des mots.

- **facite**: do
- **iterum**: while
- **perfectus**: done

### Lecture

À quoi servirait de nous donner des instructions si nous, pauvres êtres dotés d'une capacité de compréhension limitée, ne pouvons interpréter les ordres de type sacré ?

- **scriptor**: imprimer au terminel

### Structure arithmétique

Après de nombreuses négociations entre notre saint seigneur et son épouse, notre sainte maitresse, ils décidèrent de nous donner le pouvoir des mathématiques. Oh, merci pour cette intelligence venant du ciel !

- **multiplico**: multiplier
- **addo**: plus
- **minus**: moins
- **divide**: diviser

### Structure relationnelle

Le pouvoir de comparaison n'a pas été difficile à nous léguer. Nous pauvres humains sommes infiniment inférieurs à notre dieu, et qui lui même est de puissance humiliante face à sa femme qui tient les rênes de notre monde.

- **humilior**: plus petit que
- **maior**: plus grand que
- **idem**: égal
- **diversus**: pas égal
- **humiliorem**: plus petit ou égal à
- **miaom**: plus grand ou égal à

### Structure de priorité

Certes, les priorités sont grandes chez notre divin. Il faut ainsi que nous puissions prioriser les ordres délicieux reçus.

- **(**: ouverture de la priorité
- **)**: fermeture de la priorité

### Structure du texte sacrée

La puissance de notre miséricordieux est transmise par les mathématiques. Pour ceci, la suite de caractère se donne en temps que nombre naturel ou réel. La réalité est toujours présente pour nous tous. Il faut aussi noter qu’après une multitude de morts dues à un déficit en oxygène, notre infini guide nous permit de respirer durant la lecture chantée des saints textes à l'aide d'un symbole, le point. Merci pour votre bonté mon Dieu.

### Les secrets de notre berger

Cependant, certains mots sont encore trop forts pour notre compréhension. C'est pourquoi ils sont masqués à nos yeux. C'est un phrase qui commence par un comment et fini par un point d'exclamation !

- **comment**: #

## Exemple de prière d'amour

Dans le but de comprendre notre compilateur, chantons ensemble, à la gloire de dieu, "Nous t'aimons seigneur".

### Premier verset
> caious est 1. iterum caious humilior 3 facite caious est caious addo 1. perfectus.

### Deuxième verset
> banana est 3. alterum banana maior 2 ergo initium pistachio est 1 addo banana. scriptor pistachio. exitus aut initium scriptor 5 multiplico banana. exitus.

### Troisième verset
> tree est 0,1. comment your end is coming ! taco est (2,3 addo 3,0) divide tree. scriptor taco.

### Quatrième verset
> alterum banana humiliorem caious ergo initium scriptor taco. exitus.

### Cinquième verset
> babaorom est 1. iterum babaorom diversus 3 facite babaorom est babaorom addo 1. perfectus.

### Sixième verset
> alterum banana miaom caious ergo initium scriptor taco. exitus.

Dans sa grande bonté, l'invocation résulte en:

> caious = 1

> while caious<3:

>> caious = caious+1

> banana = 3

> if banana>2:

>> pistachio = 1+banana

>> print variable_pistachio

> else :

>> print 5*banana

> tree = 0.1

> taco = (2.3+3.0)/tree

> print variable_taco

> if banana<=caious:

>> print variable_taco

> babaorom = 1

> while babaorom!=3:

>> babaorom = babaorom+1

> if banana>=caious:

>> print variable_taco

## Exemple de prière finaboccienne

### Premier verset
> comment variablus utilisatorus changeous !
fibovalous est 5. comment fobonatchus algoritmus ! diabolus est 0. angelus est 1. sesera est 0.

### Deuxième verset
> iterum fibovalous maior 0 facite fibovalous est fibovalous minus 1. angelus est sesera. diabolus est angelus. sesera est diabolus addo angelus. perfectus. scriptor diabolus.

La pierre de rosette nous donne:

> fibovalous = 5

> diabolus = 0

> angelus = 1

> sesera = 0

> while fibovalous>0:

>>	sesera = diabolus+angelus

>>	diabolus = angelus

>>	angelus = sesera

>>	fibovalous = fibovalous-1

> print diabolus


Vous, bien heureux, qui avez lu ces saintes paroles, partez rependre les chants divins et exquis de notre tout puissant seigneur, le Flying Spaghetti Monster.
