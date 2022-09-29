from datetime import datetime
import json
import requests
import sys

global android
android =  hasattr(sys, 'getandroidapilevel')
if(not android):
  import pyperclip

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

def get_link(id):
  print("Getting link...")
  response = requests.get(f"https://apibay.org/t.php?id={id}")
  data = json.loads(response.content)
  return f"magnet:?xt=urn:btih:{data['info_hash']}&dn={data['name']}&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2780%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2730%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=http%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"

def copy(text):
  print("coping the link...")
  if(not android):
    pyperclip.copy(text)
  else:
    os.syem.os()
def search(q):
  url = "https://apibay.org/q.php?q=" + q

  print("\nSearching....")

  results = requests.get(url)
  data = json.loads(results.content)

  print("\n")

  # formating data
  for i in range(len(data)):
    data[i]["size"] = int(data[i]["size"]) / 1024 / 1024
    tmp = datetime.fromtimestamp(int(data[i]["added"]))
    data[i]["added"] = tmp.strftime("%d/%m/%Y %X")

  data.sort(key=lambda x: x["size"])

  for i in range(len(data)):
    name = data[i]["name"]
    size = data[i]["size"]
    date = data[i]["added"]

    if(size > 1000):
        size = str(round(size / 1024, 1)) + " Go"
    else:
      size = str(round(size)) + " Mo"

    print(f"{i + 1}) [size: {size}]  {name} ({date})")
    print("--------------------------------------------------------------------------------------------------------")
  
  selected = int(input(f"Select (1 - {len(data)}): ")) - 1
  id = int(data[selected]["id"])
  link = get_link(id)
  copy(link)
  print("Link: ", link)
  

search(entrer_q())