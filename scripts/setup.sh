#!/bin/bash

echo "Mise en place de l'environnement..."

# On vérifie si Python est installé.
if command -v python3 &>/dev/null; then
    echo "Python3 est installé."
else
	echo "Python3 n'est pas installé."
	exit 1
fi

# On vérifie si pip est installé.
if command -v pip3 &>/dev/null; then
	echo "pip est installé."
else
	echo "pip n'est pas installé."
	exit 1
fi