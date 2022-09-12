from datetime import datetime
import json
import requests


def format_name(name):
  return name.strip().replace(" ", "+").lower()

def entrer_q():
  type = int(input("1. TV show\n2. Movie\n\nEnter your choice: "))

  if type == 1:
    show = input("Show: ")
    saison = int(input("Saison: "))

    if(saison == 0):
      q = format_name(show) + "&cat=208"
    
    else:
      episode = int(input("Episode: "))

      saison = "0" + str(saison) if saison < 10 else saison
      episode = "0" + str(episode) if episode < 10 else episode
      q = f"{format_name(show)}+s{saison}e{episode}&cat=208"
  
  else:
    movie = input("Movie: ")
    q = f"{format_name(movie)}&cat=207"
  
  return q

def search(q):
  url = "https://apibay.org/q.php?q=" + q

  print("\nSearching....")

  results = requests.get(url)
  data = json.loads(results.content)

  print("\n")

  for result in data:
    name = result["name"]
    size = int(result["size"]) / 1024 / 1024
    _date = datetime.fromtimestamp(int(result["added"]))
    _date = _date.strftime("%d/%m/%Y %X")

    if(size > 1000):
        size = str(round(size / 1024, 1)) + " Go"
    else:
      size = str(round(size)) + " Mo"

    print(f"[size: {size}]  {name} ({_date})")
    print("--------------------------------------------------------------------------------------------------------")

search(entrer_q())