import xml.etree.ElementTree as ET
import csv

# XML file path
xml_file = 'updated_combined_tables.xml'

# Parse the XML
tree = ET.parse(xml_file)
root = tree.getroot()

# CSV file path
csv_file = 'tables_list.csv'

# Open CSV file for writing
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the header
    writer.writerow(["Name", "Description"])

    # Iterate through each table in the XML
    for table in root.findall('table'):
        name = table.get('name')
        description = table.get('description')

        # Write the table name and description to the CSV
        writer.writerow([name, description])

print(f"CSV file '{csv_file}' created successfully.")
