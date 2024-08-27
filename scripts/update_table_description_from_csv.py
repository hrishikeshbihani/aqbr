import xml.etree.ElementTree as ET
import csv

# Input file paths
csv_file = 'tables_list.csv'  # Input CSV file with updated descriptions
xml_file = 'updated_combined_tables.xml'       # Input XML file to be updated
# Output XML file with updated descriptions
output_xml_file = 'updated_combined_tables.xml'

# Parse the XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Read the CSV and update the XML descriptions
with open(csv_file, mode='r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        table_name = row['Name']
        new_description = row['Description']

        # Find the table in the XML and update its description
        for table in root.findall('table'):
            if table.get('name') == table_name:
                table.set('description', new_description)
                break

# Write the updated XML to a new file
tree.write(output_xml_file)

print(f"XML file '{output_xml_file}' updated successfully.")
