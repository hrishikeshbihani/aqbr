import xml.etree.ElementTree as ET

def remove_dimensions_from_xml(input_file, output_file):
    # Parse the input XML file
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Iterate through all 'table' elements
    for table in root.findall('table'):
        # Find the 'dimensions' element and remove it
        dimensions = table.find('dimensions')
        if dimensions is not None:
            table.remove(dimensions)

    # Write the modified XML to the output file
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"New XML file with dimensions removed has been written to {output_file}")


# File paths
input_file = './combined_tables_copy.xml'
output_file = 'output_without_dimensions.xml'

# Remove dimensions from XML and save the result
remove_dimensions_from_xml(input_file, output_file)
