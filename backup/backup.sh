#!/bin/bash

# Répertoire contenant les fichiers à sauvegarder
minecraft_dir="/srv/minecraft-data/$1"

# Répertoire de destination des sauvegardes
# TODO : Pour la backup dir il faut utiliser le STFP (192.168.1.2)
backup_dir="/home/wiibleyde/backup/"

# Nom de base des archives de sauvegarde
backup_name="minecraft_backup"

# Nombre maximum d'archives de sauvegarde à conserver
max_backups=5

# Itération pour créer une nouvelle sauvegarde
for i in $(seq 1 $max_backups)
do
    # Nom de l'archive de sauvegarde avec la date et l'heure
    backup_file="$backup_name-$(date +%Y-%m-%d_%H-%M-%S).tar.gz"
    
    # Création de l'archive de sauvegarde
    tar -czvf "$backup_dir/$backup_file" \
        "$minecraft_dir/banned-ips.json" \
        "$minecraft_dir/banned-players.json" \
        "$minecraft_dir/ops.json" \
        "$minecraft_dir/server.properties" \
        "$minecraft_dir/whitelist.json" \
        "$minecraft_dir/world/" \
        "$minecraft_dir/usercache.json"

    # Affichage d'un message de confirmation
    echo "La sauvegarde de Minecraft a été créée avec succès dans $backup_dir/$backup_file"
    
    # Si on a dépassé le nombre maximal d'archives à conserver
    if [ $(ls -1 "$backup_dir" | grep "$backup_name-" | wc -l) -gt $max_backups ]
    then
        # Suppression de la plus ancienne archive de sauvegarde
        oldest_backup=$(ls -1t "$backup_dir" | grep "$backup_name-" | tail -1)
        rm "$backup_dir/$oldest_backup"
        echo "La sauvegarde la plus ancienne ($oldest_backup) a été supprimée"
    fi
done