import yaml
import sys

try:
    with open(r"c:\Users\josse\Documents\Proyectos\PHCCC\ERPNext-PHCCC\.coolify\docker-compose - funcional 3 - Full.yaml", 'r') as f:
        yaml.safe_load(f)
    print("YAML is valid")
except Exception as e:
    print(f"YAML Error: {e}")
