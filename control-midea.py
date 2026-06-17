import time
from midealocal.discover import discover
from midealocal.devices import device_selector

token = '9da03d4a3d20ae76ae8933549a4d1884a5ca95249dc0d913ecdd7704ae7e16c1351073a3d40e2f749de31e4d15db395d49302699fdf26ac662642db698f60c6c'
key = 'f5f759ff59954ba59e727e15999716dccb4c2b2fd2a04fb1b26d070ee609197c'

# 1. Découverte de l'appareil
discover_results = list(discover(ip_address="192.168.1.192").values())[0]

if isinstance(discover_results, list):
    d = discover_results[0]
else:
    d = discover_results

# 2. Création de l'appareil
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

# 3. Création de la fonction qui va recevoir les données
def on_update(status_dict):
    """Cette fonction sera appelée automatiquement à chaque fois que la clim envoie des infos."""
    print(f"\n--- NOUVELLES DONNÉES REÇUES ---")
    if "indoor_temperature" in status_dict:
        print(f"Température intérieure : {status_dict['indoor_temperature']}°C")
    if "power" in status_dict:
        print(f"La clim est allumée : {status_dict['power']}")
    print("--------------------------------\n")

# 4. On indique à la clim d'utiliser notre fonction
ac.register_update(on_update)

# 5. On connecte ET ON DÉMARRE LE THREAD D'ÉCOUTE en tâche de fond
ac.connect(check_protocol=True)
ac.open() # DÉMARRE L'ÉCOUTE (Très important)

print("En attente de connexion et des premières données...")

# On laisse le temps au thread d'arrière-plan de se connecter et de recevoir le 1er message
time.sleep(5) 

# Si vous voulez forcer une mise à jour manuellement :
# ac.refresh_status() 

print("\nEnvoi de la commande pour éteindre la climatisation...")
ac.set_attribute("power", True)

# On laisse 3 secondes au thread pour envoyer la commande et recevoir la confirmation
time.sleep(3)

print("Fermeture du script et de la connexion.")
# 6. On ferme proprement le thread d'écoute avant de quitter
ac.close()