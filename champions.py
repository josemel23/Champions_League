from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Configuración del driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL objetivo
url = "https://www.apwin.com/league/europe/uefa-champions-league/standings/"
driver.get(url)

# Esperar a que cargue la página completamente
time.sleep(5)

# Extraer datos de la tabla
table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
standings = []

for row in table_rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    if columns:
        # Verificar si la fila contiene datos válidos
        if columns[0].text.strip() and columns[1].text.strip():
            team_data = {
                "position": columns[0].text.strip(),
                "team": columns[1].text.strip(),
                "matches_played": columns[2].text.strip(),
                "wins": columns[3].text.strip(),
                "draws": columns[4].text.strip(),
                "losses": columns[5].text.strip(),
                "goals_for": columns[6].text.strip(),
                "goals_against": columns[7].text.strip(),
                "goal_difference": columns[8].text.strip(),
                "points": columns[9].text.strip()
            }
            standings.append(team_data)

# Guardar los datos en formato JSON
output_file = "Champions_League_standings.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(standings, f, ensure_ascii=False, indent=4)

print(f"Datos guardados en {output_file}")

# Cerrar el navegador
driver.quit()
