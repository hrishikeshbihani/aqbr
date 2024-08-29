import xml.etree.ElementTree as ET
import csv

# Input file paths
csv_file = 'table_descriptions.csv'  # Input CSV file with updated descriptions
xml_file = 'combined_tables.xml'  # Input XML file to be updated
# Output XML file with updated descriptions
output_xml_file = 'combined_tables.xml'

# Parse the XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Read the CSV and update the XML descriptions
updated_table_names = set()
csv_data = {}

with open(csv_file, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        table_name = row['TableName']
        new_description = row['Description']
        updated_table_names.add(table_name)
        csv_data[table_name] = new_description

        # Find the table in the XML and update its description
        table_found = False
        for table in root.findall('table'):
            if table.get('name') == table_name:
                table.set('description', new_description)
                table_found = True
                break

        # If the table was not found, add it as a new entry
        if not table_found:
            new_table = ET.SubElement(
                root, 'table', name=table_name, description=new_description)
            ET.SubElement(new_table, 'metrics')  # Add empty metrics section
            # Add empty dimensions section
            ET.SubElement(new_table, 'dimensions')

# Remove tables from XML that are not in the CSV
for table in root.findall('table'):
    table_name = table.get('name')
    if table_name not in updated_table_names:
        root.remove(table)

# Write the updated XML to a new file
tree.write(output_xml_file, encoding='utf-8', xml_declaration=True)

print(f"XML file '{output_xml_file}' updated successfully.")
