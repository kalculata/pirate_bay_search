import sys
import json
import requests
from os import system
from enum import Enum
from datetime import datetime

global android
android =  hasattr(sys, 'getandroidapilevel')
if(not android):
  import pyperclip

choice            = -1
film_category_id  = 207
serie_category_id = 208
base_url          = "https://apibay.org/q.php?q="


class Content(Enum):
  SERIE = 1
  FILM  = 2


def menu():
  print("\n")
  print("1. Series")
  print("2. Films")
  print("3. Quit")

def complete_serie_title(title):
  saison = int(input("Saison: "))
      
  if saison > 0:
    title   = title + "s" + str(saison)
    episode = int(input("Episode"))

    if episode > 0:
      e     = "0" + str(episode) if episode < 10 else str(episode)
      title = title + "e" + e

  return title

def search(title, query):
  url = base_url + query

  print(f"\nSearching ({title})...")
  results = requests.get(url)
  data    = json.loads(results.content)

  # formating data
  for i in range(len(data)):
    data[i]["size"]  = int(data[i]["size"]) / 1024 / 1024
    tmp              = datetime.fromtimestamp(int(data[i]["added"]))
    data[i]["added"] = tmp.strftime("%d/%m/%Y %X")

  # choice order by column
  selected = -1
  while selected == -1:
    sort_column = "size"
    t = input("Order by (name, size, added | default = size): ")
    if len(t) > 0 or t in ["name", "size", "added"]:
      sort_column = t
    data.sort(key=lambda x: x[sort_column])

    print("\n")

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

  if selected > -1:
    id       = int(data[selected]["id"])
    link     = get_link(id)
    copy(link)

def get_link(id):
  print("Getting link...")
  response = requests.get(f"https://apibay.org/t.php?id={id}")
  data     = json.loads(response.content)
  return f"magnet:?xt=urn:btih:{data['info_hash']}&dn={data['name']}&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2780%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2730%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=http%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce"

def copy(text):
  if(not android):
    pyperclip.copy(text)
  else:
    system(f'termux-clipboard-set "{text}"')
  print("LINK COPIED IN YOUR CLIPBOARD, YOU CAN NOW PASTE IT.")

if __name__ == "__main__":
  while choice != 3:
    menu()
    choice = int(input("\nEnter your choice: "))

    if choice != 3:
      title      = input("\nTitle: ").strip().replace(" ", "+").lower()
      query      = ""

      if   choice == Content.FILM.value:
        query = title + "&cat=" + str(film_category_id)
      elif choice == Content.SERIE.value:
        title      = complete_serie_title(title)
        query      = title + "&cat=" + str(serie_category_id)

      search(title, query)