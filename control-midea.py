import time
from datetime import datetime
from midealocal.discover import discover
from midealocal.devices import device_selector

# Identifiants
token = '9da03d4a3d20ae76ae8933549a4d1884a5ca95249dc0d913ecdd7704ae7e16c1351073a3d40e2f749de31e4d15db395d49302699fdf26ac662642db698f60c6c'
key = 'f5f759ff59954ba59e727e15999716dccb4c2b2fd2a04fb1b26d070ee609197c'

# --- 1. DÉCOUVERTE ET CONNEXION ---
discover_results = list(discover(ip_address="192.168.1.192").values())[0]

if isinstance(discover_results, list):
    d = discover_results[0]
else:
    d = discover_results

ac = device_selector(
  name="AC",
  device_id=d['device_id'],
  device_type=d['type'],
  ip_address=d['ip_address'],
  port=d['port'],
  token=token,
  key=key,
  device_protocol=d['protocol'],
  model=d['model'],
  subtype=0,
  customize="",
)

ac.connect(check_protocol=True)
ac.open() # Démarrage de l'écoute

print("Connexion en cours, récupération de l'état actuel...")
time.sleep(5) # On laisse 5 secondes au script pour recevoir l'état actuel de la clim

# --- 2. RÉCUPÉRATION DES VARIABLES NÉCESSAIRES ---

# L'état actuel de la clim (True = Allumée, False = Éteinte)
is_on = ac._attributes.get("power")

# La date et l'heure actuelles
maintenant = datetime.now()
heure_actuelle = maintenant.hour
jour_semaine = maintenant.weekday() # 0 = Lundi, 1 = Mardi... 5 = Samedi, 6 = Dimanche

# Variable de présence (À remplacer par votre vrai système de détection)
personne_au_bureau = True 

print(f"-> Il est {heure_actuelle}h")
print(f"-> Jour de la semaine : {jour_semaine} (0=Lundi, 6=Dimanche)")
print(f"-> État de la clim : {'Allumée' if is_on else 'Éteinte'}")
print("-" * 30)

# --- 3. LOGIQUE CONDITIONNELLE ---

# Condition A : S'il n'y a personne au bureau, on éteint la clim
if not personne_au_bureau:
    if is_on: # Inutile d'envoyer la commande si elle est déjà éteinte
        print("Action : Personne au bureau détecté. Extinction de la clim.")
        ac.set_attribute("power", False)
        time.sleep(2)
    else:
        print("Personne au bureau, mais la clim est déjà éteinte.")

# Condition B : Si elle est allumée et qu'il est 12h (entre 12h00 et 12h59) on éteint
elif is_on and heure_actuelle == 12:
    print("Action : Il est midi, c'est la pause. Extinction de la clim.")
    ac.set_attribute("power", False)
    time.sleep(2)

# Condition C : S'il est 9h (entre 9h00 et 9h59) ET jour de semaine (0 à 4 = Lundi à Vendredi) on allume
elif heure_actuelle == 9 and jour_semaine < 5:
    if not is_on: # Inutile de l'allumer si elle tourne déjà
        print("Action : Il est 9h en semaine. Allumage de la clim.")
        ac.set_attribute("power", True)
        time.sleep(2)
    else:
        print("Il est 9h en semaine, mais la clim est déjà allumée.")

# Si aucune condition n'est remplie
else:
    print("Aucune action n'est requise à cette heure-ci.")


# --- 4. FERMETURE PROPRE ---
print("Fermeture de la connexion.")
ac.close()