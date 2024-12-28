from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# Configuración del driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# URL objetivo
url = "https://www.apwin.com/league/europe/uefa-champions-league/standings/corners//"
driver.get(url)

# Esperar a que cargue la página completamente
time.sleep(5)

# Extraer datos de la tabla
table_rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
corner_stats = []

for row in table_rows:
    columns = row.find_elements(By.TAG_NAME, "td")
    if columns:
        # Verificar si la fila contiene datos válidos
        if columns[0].text.strip() and columns[1].text.strip():
            team_data = {
                "position": columns[0].text.strip(),
                "team": columns[1].text.strip(),
                "corners": {
                    "8.5": columns[4].text.strip(),
                    "9.5": columns[5].text.strip(),
                    "10.5": columns[6].text.strip(),
                    "11.5": columns[7].text.strip(),
                    "12.5": columns[8].text.strip(),
                    "13.5": columns[9].text.strip(),
                    "average": columns[10].text.strip()
                }
            }
            corner_stats.append(team_data)

# Guardar los datos en formato JSON
output_file = "Champions_League_corners.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(corner_stats, f, ensure_ascii=False, indent=4)

print(f"Datos guardados en {output_file}")

# Cerrar el navegador
driver.quit()
