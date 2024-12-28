import json
import random
import math

def simulate_corners(team_stats):
    """
    Simula estadísticas de corners basadas en la posición y goles marcados del equipo.
    """
    goals_for = int(team_stats['goals_for'])
    matches = int(team_stats['matches_played'])
    position = int(team_stats['position'])
    
    # Base de corners calculada según goles por partido y posición
    base_corners = (goals_for / matches) * 2 + (37 - position) / 3
    
    # Añadir variabilidad aleatoria (±1.5 corners)
    average_corners = round(base_corners + random.uniform(-1.5, 1.5), 2)
    
    # Asegurar que el promedio está entre 8 y 13
    average_corners = max(8, min(13, average_corners))
    
    # Calcular probabilidades para cada umbral
    corners_data = {
        "8.5": str(min(100, round((average_corners - 7) / average_corners * 100))) + "%",
        "9.5": str(min(100, round((average_corners - 8) / average_corners * 100))) + "%",
        "10.5": str(min(100, round((average_corners - 9) / average_corners * 100))) + "%",
        "11.5": str(min(100, round((average_corners - 10) / average_corners * 100))) + "%",
        "12.5": str(min(100, round((average_corners - 11) / average_corners * 100))) + "%",
        "13.5": str(min(100, round((average_corners - 12) / average_corners * 100))) + "%",
        "average": str(average_corners)
    }
    
    return corners_data

def process_teams(positions_data, corners_data):
    """
    Procesa los datos de equipos y genera/actualiza estadísticas de corners.
    """
    # Crear diccionario de corners existentes
    existing_corners = {team['team']: team['corners'] for team in corners_data}
    
    new_corners_data = []
    position = 1
    
    for team in positions_data:
        team_name = team['team']
        
        # Si el equipo ya tiene datos de corners, usarlos
        if team_name in existing_corners:
            corners = existing_corners[team_name]
        else:
            # Si no, simular nuevos datos
            corners = simulate_corners(team)
        
        new_corners_data.append({
            "position": str(position),
            "team": team_name,
            "corners": corners
        })
        position += 1
    
    return new_corners_data

def update_corners_data():
    """
    Lee y actualiza los datos de corners usando los nombres de archivo correctos.
    """
    try:
        # Leer datos de posiciones
        with open('Champions_League_standings.json', 'r', encoding='utf-8') as f:
            positions_data = json.load(f)
        
        # Leer datos de corners existentes
        with open('Champions_League_corners.json', 'r', encoding='utf-8') as f:
            corners_data = json.load(f)
        
        # Procesar y actualizar datos
        updated_data = process_teams(positions_data, corners_data)
        
        # Guardar datos actualizados
        with open('Champions_League_corners.json', 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=4)
        
        print("Datos de corners actualizados exitosamente")
        
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo: {e.filename}")
    except Exception as e:
        print(f"Error durante el procesamiento: {str(e)}")

if __name__ == "__main__":
    update_corners_data()