#!/usr/bin/env python3
import csv
import json
import os
import sys

# Ensure repository root is on sys.path so we can import ejemplos_uso (adjust if your layout differs)
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)

from ejemplos_uso import ejemplo_automatizacion  # noqa: E402


def test_ejemplo_automatizacion_creates_json(tmp_path):
    """
    Smoke test for ejemplo_automatizacion:
    - create a small CSV with one transaction
    - run ejemplo_automatizacion using that CSV
    - assert an output JSON exists and contains expected keys/values
    """
    sample_csv = tmp_path / "datos_enero.csv"
    out_json = tmp_path / "analisis_multiple.json"

    # create a minimal CSV with headers used by the examples
    with sample_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "fecha",
                "id_cliente",
                "nombre_cliente_final",
                "ciudad",
                "id_producto",
                "nombre_producto",
                "categoria_redefinida",
                "cantidad",
                "importe",
                "medio_pago",
            ]
        )
        writer.writerow(
            ["2024-01-15", "1", "Juan Pérez", "Madrid", "101", "Producto A", "Electrónicos", "2", "200.50", "tarjeta"]
        )

    # Run the example automation with explicit inputs/outputs so we don't touch repo files
    ejemplo_automatizacion(input_files=[str(sample_csv)], output_json=str(out_json))

    assert out_json.exists(), "Expected output JSON to be created"

    with out_json.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert isinstance(data, list), "Output JSON should be a list"
    assert len(data) == 1, "Expected one summary in the output list"

    item = data[0]
    assert "archivo" in item and item["archivo"].endswith("datos_enero.csv")
    assert "registros" in item and item["registros"] == 1
    # total_ventas numeric check (float equality for this simple sample)
    assert "total_ventas" in item and abs(item["total_ventas"] - 200.5) < 1e-6
