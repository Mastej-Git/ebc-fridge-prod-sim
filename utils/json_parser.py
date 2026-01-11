import json
from typing import Any


def parse_bodys_json(file_path: str) -> list[dict[str, Any]]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {str(e)}")
        return []
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def format_bodys_data(data: List[Dict[str, Any]]) -> str:
    output = []

    for idx, item in enumerate(data, 1):
        output.append(f"{'='*60}")
        output.append(f"BODY #{idx}")
        output.append(f"{'='*60}")

        if 'body' in item:
            body = item['body']

            # Framework
            if 'framework' in body:
                output.append("\nFramework:")
                output.append(f"  Material: {body['framework'].get('material', 'N/A')}")
                output.append(f"  Color: {body['framework'].get('color', 'N/A')}")

            # Upper Panel
            if 'upper_panel' in body:
                output.append("\nUpper Panel:")
                output.append(f"  Controllable: {body['upper_panel'].get('is_controllable', 'N/A')}")
                output.append(f"  Type: {body['upper_panel'].get('type', 'N/A')}")

            # Middle Panel
            if 'middle_panel' in body:
                output.append("\nMiddle Panel:")
                output.append(f"  Functionality: {body['middle_panel'].get('functionality', 'N/A')}")

            # Lower Panel
            if 'lower_panel' in body:
                output.append("\nLower Panel:")
                output.append(f"  Functionality: {body['lower_panel'].get('functionality', 'N/A')}")
                output.append(f"  Cup Holder: {body['lower_panel'].get('is_cup', 'N/A')}")
                output.append(f"  Color: {body['lower_panel'].get('color', 'N/A')}")

            # Armrest
            if 'armrest' in body:
                output.append("\nArmrest:")
                output.append(f"  Heating: {body['armrest'].get('heating', 'N/A')}")
                output.append(f"  Material: {body['armrest'].get('material', 'N/A')}")
                output.append(f"  Color: {body['armrest'].get('color', 'N/A')}")

            # Cup Holder
            if 'cup_holder' in body:
                output.append("\nCup Holder:")
                output.append(f"  USB Socket: {body['cup_holder'].get('usb_socket', 'N/A')}")
                output.append(f"  Color: {body['cup_holder'].get('color', 'N/A')}")

        output.append("")

    return "\n".join(output)
