# /run generate-example-inputs
name: generate-example-inputs
description: Vytvoří ukázkový CSV soubor se vstupními daty pro simulátor potrubí.
parameters:
  - name: file
    description: Název výstupního CSV souboru
    type: string
    required: false
    default: potrubi.csv
run: |
  import csv

  rows = [
      ["section_id", "length_m", "diameter_mm", "roughness_mm", "type", "local_loss_k"],
      [1, 12, 100, 0.1, "pipe", ""],
      [2, "", "", "", "elbow", 0.75],
      [3, 6, 80, 0.05, "pipe", ""],
      [4, "", "", "", "valve", 1.5]
  ]

  with open(file, "w", newline="") as f:
      writer = csv.writer(f)
      writer.writerows(rows)

  print(f"Ukázkový vstupní soubor uložen jako {file}")