import xml.etree.ElementTree as ET
import csv

# Input files and variables
input_xml_file_path = 'all_tables.xml'  # Path to the original XML file
# Path to the CSV file mapping tables to categories
input_csv_file_path = 'table_category_map.csv'
output_xml_file_path = 'category_table_map.xml'  # Path for the output XML file

# Load the original XML file
original_xml_tree = ET.parse(input_xml_file_path)
original_xml_root = original_xml_tree.getroot()

# Load the CSV file mapping tables to categories
table_to_category_map = {}
with open(input_csv_file_path, mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    csv_headers = next(csv_reader)  # Skip the header row
    for row in csv_reader:
        table_name = row[0]
        associated_categories = [csv_headers[i]
                                 for i in range(1, len(row)) if row[i] == 'TRUE']
        table_to_category_map[table_name] = associated_categories

# Create the new XML structure
categories_root_element = ET.Element('Categories')

# Iterate over the categories and build the XML
for category_name in csv_headers[1:]:
    category_element = ET.SubElement(
        categories_root_element, 'Category', name=category_name)
    tables_element = ET.SubElement(category_element, 'Tables')

    for table_name, table_categories in table_to_category_map.items():
        if category_name in table_categories:
            # Find the corresponding table schema in the original XML
            table_schema_element = original_xml_root.find(
                f"./table[@name='{table_name}']")
            if table_schema_element is not None:
                # Add the table schema to the current category
                table_element = ET.SubElement(
                    tables_element, 'Table', name=table_name)
                table_element.extend(table_schema_element)

# Write the new XML structure to a file
categorized_xml_tree = ET.ElementTree(categories_root_element)
categorized_xml_tree.write(
    output_xml_file_path, encoding='utf-8', xml_declaration=True)

print(f"New XML file '{output_xml_file_path}' has been created successfully.")
