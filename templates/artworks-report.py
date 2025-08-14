import argparse
import requests
import json
from fpdf import FPDF
from datetime import datetime

# --- Función para hacer la petición a la API ---
def fetch_artworks(search_term, fields, limit):
    base_url = "https://api.artic.edu/api/v1/artworks/search"
    params = {
        "q": search_term,
        "fields": ",".join(fields),
        "limit": limit
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    return data["data"]

# --- Función para guardar en JSON ---
def save_json(artworks, filename="artworks_report.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(artworks, f, indent=4, ensure_ascii=False)
    print(f"✅ Archivo JSON generado: {filename}")

# --- Función para guardar en PDF ---
def save_pdf(artworks, fields, filename="artworks_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_title("Artworks Report - Art Institute of Chicago")
    pdf.cell(200, 10, txt="Reporte de Obras - Instituto de Arte de Chicago", ln=True, align="C")
    pdf.ln(10)

    for idx, artwork in enumerate(artworks, start=1):
        pdf.set_font("Arial", style='B', size=11)
        pdf.cell(200, 10, txt=f"Obra #{idx}", ln=True)
        pdf.set_font("Arial", size=10)
        for field in fields:
            value = artwork.get(field, "N/A")
            pdf.multi_cell(0, 8, txt=f"{field}: {value}")
        pdf.ln(5)

    pdf.output(filename)
    print(f"✅ Archivo PDF generado: {filename}")

# --- Función principal ---
def main():
    parser = argparse.ArgumentParser(description="Script para generar reportes de obras del Instituto de Arte de Chicago")
    parser.add_argument('--search', type=str, required=True, help='Palabra clave para filtrar obras por metadatos.')
    parser.add_argument('--fields', nargs='+', required=True, help='Campos a incluir en el reporte.')
    parser.add_argument('--artworks', type=int, required=True, help='Cantidad de obras a recuperar.')

    args = parser.parse_args()

    try:
        print("🔍 Buscando obras...")
        artworks = fetch_artworks(args.search, args.fields, args.artworks)
        if not artworks:
            print("⚠️ No se encontraron obras con los criterios especificados.")
            return

        save_json(artworks)
        save_pdf(artworks, args.fields)

    except requests.RequestException as e:
        print(f"❌ Error al conectarse a la API: {e}")
    except Exception as e:
        print(f"❌ Error general: {e}")

if __name__ == "__main__":
    main()
