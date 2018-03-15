printf "Démarrage du FTW-Bot.\n"
printf "\nMise a jour des dépendance...\n"
if [ "$EUID" -ne 0 ]
  then echo "Pour que le bot fonctionne correctement, merci de le lancer en root !"
  exit
fi
  python3.6 -m pip install --upgrade Discord
  python3.6 -m pip install --upgrade PyNaCl
  python3.6 -m pip install --upgrade youtube_dl
  printf "\nMise a jour terminer !\n"
  printf "\nLancement du FTW-Bot...\n"
  python3.6 bot.py