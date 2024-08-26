import xml.etree.ElementTree as ET

# Input XML file path
xml_file_path = './all_tables.xml'

# Step 1: Load and parse the XML data
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Step 2: Extract unique table names
table_names = set()
for table in root.findall('table'):
    table_name = table.get('name')
    if table_name:
        table_names.add(table_name)

# Step 3: Print the list of unique table names
print("Unique table names:")
for name in sorted(table_names):
    print(name)
