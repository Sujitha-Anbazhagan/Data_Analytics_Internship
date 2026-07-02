import json

for notebook_file in ["01_EDA.ipynb", "02_model_building.ipynb"]:
    with open(notebook_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check raw content for the exact string
    if "df['Churn'].value_counts()" in content:
        print(f"Found in {notebook_file}")
        # Find the cell
        nb = json.loads(content)
        for i, cell in enumerate(nb["cells"]):
            source = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
            if "df['Churn'].value_counts()" in source:
                print(f"  Cell {i} contains the string")
                print(f"  Cell ID: {cell.get('id', 'N/A')}")
    else:
        print(f"Not found in {notebook_file}")
