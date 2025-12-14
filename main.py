# We maken gebruik van de openai module, zorg dat deze geïnstalleerd is
import os
import json
import datetime
import sys

# Probeer OpenAI te importeren, geef duidelijke foutmelding als het mist
try:
    import openai
except ImportError:
    print("❌ Installeer eerst de openai module: pip install openai")
    sys.exit()

# --- CONFIGURATIE ---
# Haalt de key uit je omgeving of secrets. 
# Als je dit lokaal draait, zorg dat je een environment variable 'OPENAI_API_KEY' hebt.
API_KEY = os.getenv("OPENAI_API_KEY") 
DATA_FILE = "mijn_ideeen.json"

# Kleuren voor de terminal (werkt in de meeste consoles)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- FUNCTIES ---

def get_client():
    """Maak een verbinding met de OpenAI API."""
    if not API_KEY:
        print(f"{Colors.FAIL}FOUT: Geen API Key gevonden.{Colors.ENDC}")
        print("Zet je key in de code of gebruik 'export OPENAI_API_KEY=sk-...'")
        return None
    openai.api_key = API_KEY
    return openai

def ask_ai_brain():
    """Stel een vraag aan GPT-3 voor code advies."""
    client = get_client()
    if not client: return

    print(f"\n{Colors.HEADER}🧠 AI Developer Brain (Type 'exit' om te stoppen){Colors.ENDC}")
    
    while True:
        vraag = input(f"{Colors.BLUE}Vraag: {Colors.ENDC}")
        if vraag.lower() in ['exit', 'stop', 'q']:
            break
            
        print(f"{Colors.WARNING}Denken...{Colors.ENDC}")
        
        try:
            response = client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Jij bent een Senior Python Expert. Geef kort, bondig en technisch correct antwoord."},
                    {"role": "user", "content": vraag}
                ]
            )
            antwoord = response.choices[0].message.get('content', 'Geen antwoord ontvangen')
            print(f"\n{Colors.GREEN}>> {antwoord}{Colors.ENDC}\n")
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")

def save_idea():
    """Sla een idee of snippet op in een JSON bestand."""
    print(f"\n{Colors.HEADER}📝 Idee Opslaan{Colors.ENDC}")
    titel = input("Titel: ")
    inhoud = input("Omschrijving/Snippet: ")
    
    entry = {
        "datum": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "titel": titel,
        "inhoud": inhoud
    }
    
    # Bestaande data laden
    data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                data = json.load(f)
            except:
                data = []
    
    data.append(entry)
    
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
        
    print(f"{Colors.GREEN}✅ Opgeslagen in {DATA_FILE}!{Colors.ENDC}")

def scaffold_project():
    """Maakt automatisch een projectmap structuur aan."""
    print(f"\n{Colors.HEADER}📂 Project Scaffolder{Colors.ENDC}")
    naam = input("Projectnaam (geen spaties): ")
    
    if os.path.exists(naam):
        print(f"{Colors.FAIL}Map bestaat al!{Colors.ENDC}")
        return

    # De structuur die we maken
    mappen = [f"{naam}/src", f"{naam}/tests", f"{naam}/docs"]
    bestanden = {
        f"{naam}/README.md": f"# {naam}\n\nProject aangemaakt met DevTool.",
        f"{naam}/requirements.txt": "openai\nrequests",
        f"{naam}/src/main.py": "def main():\n    print('Hello World')\n\nif __name__ == '__main__':\n    main()",
        f"{naam}/.gitignore": "__pycache__/\n.env\n.DS_Store"
    }
    
    # Uitvoeren
    try:
        os.makedirs(naam)
        for map_naam in mappen:
            os.makedirs(map_naam)
            
        for pad, inhoud in bestanden.items():
            with open(pad, 'w') as f:
                f.write(inhoud)
                
        print(f"{Colors.GREEN}✅ Project '{naam}' is klaar voor gebruik!{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Er ging iets mis: {e}{Colors.ENDC}")

def show_menu():
    print(f"\n{Colors.BOLD}--- MIJN DEV TOOL ---{Colors.ENDC}")
    print("1. 🧠 Vraag de AI (GPT-3.5)")
    print("2. 📝 Notitie/Idee opslaan")
    print("3. 📂 Nieuw Project Opzetten (Scaffold)")
    print("4. 🚪 Afsluiten")

# --- MAIN LOOP ---
def main():
    print(f"{Colors.GREEN}Welkom terug, Developer.{Colors.ENDC}")
    
    while True:
        show_menu()
        keuze = input(f"\n{Colors.BLUE}Keuze [1-4]: {Colors.ENDC}")
        
        if keuze == '1':
            ask_ai_brain()
        elif keuze == '2':
            save_idea()
        elif keuze == '3':
            scaffold_project()
        elif keuze == '4':
            print("👋 Tot de volgende keer.")
            break
        else:
            print("Ongeldige keuze.")

if __name__ == "__main__":
    main()
