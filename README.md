# Mutant Detector

Este proyecto es una API REST para detectar si un humano es un mutante basado en su secuencia de ADN.

## Instalación

1. Clona el repositorio: git clone https://github.com/tu-usuario/mutant-detector.git

2. Activa el entorno virtual y luego instala las dependencias:
   cd mutant-detector python -m venv mutant-env mutant-env\Scripts\activate # En Windows source mutant-env/bin/activate # En Mac/Linux pip install -r requirements.txt

3. Ejecuta el servidor:

## Uso

Utiliza una herramienta como Postman para realizar solicitudes POST al endpoint `/mutant` con el siguiente formato JSON:

```json
{
"dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
}
Copiar código
```
