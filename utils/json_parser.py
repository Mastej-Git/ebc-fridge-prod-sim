import json
from typing import Any
from fridge_parts.Fridge import Fridge
from fridge_parts.Cover import Cover
from fridge_parts.Doors import Doors
from fridge_parts.Shelves import Shelves
from fridge_parts.CoolingSystem import CoolingSystem
from fridge_parts.Lights import Lights


def parse_bodys_json(file_path: str) -> list[Fridge]:
    """Load JSON file and convert directly to Fridge objects."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            if 'body' in data:
                items = [data]
            else:
                items = list(data.values())
        else:
            items = [data] if data else []
        
        fridges = []
        for item in items:
            if isinstance(item, dict) and 'body' in item:
                try:
                    fridge = _create_fridge(item)
                    fridge.check_parts_activation()
                    fridges.append(fridge)
                    # print(fridge) # For debugging purposes
                except Exception as e:
                    print(f"Error creating fridge object: {e}")
                    continue
        
        return fridges
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {str(e)}")
        return []
    except Exception as e:
        print(f"Error: {str(e)}")
        return []


def _create_fridge(item: dict) -> Fridge:
    """Create a Fridge object from dictionary data."""
    body_id = item.get('id', 1)
    body = item.get('body', {})
    
    cover_data = body.get('cover', {})
    cover = Cover(
        material=cover_data.get('material', 'N/A'),
        color=cover_data.get('color', 'N/A')
    )
    
    doors_data = body.get('doors', {})
    doors = Doors(
        material=doors_data.get('material', 'N/A'),
        machine=doors_data.get('machine', 'N/A'),
        front_panel=doors_data.get('front_panel', False)
    )
    
    shelves_data = body.get('shelves', {})
    shelves = Shelves(
        material=shelves_data.get('material', 'N/A'),
        quantity=shelves_data.get('number', 0),
        adjustable=shelves_data.get('adjustable_height', False)
    )
    
    cooling_data = body.get('cooling_system', {})
    cooling_system = CoolingSystem(
        type=cooling_data.get('type', 'N/A'),
        energy_class=cooling_data.get('energy_class', 'N/A')
    )
    
    lighting_data = body.get('lighting', {})
    lights = Lights(
        type=lighting_data.get('internal_lights', 'N/A'),
        automatic=lighting_data.get('automatic_light_on', False)
    )
    
    return Fridge(
        body_id=body_id,
        cover=cover,
        doors=doors,
        shelves=shelves,
        cooling_system=cooling_system,
        lights=lights
    )