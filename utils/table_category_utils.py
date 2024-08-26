import xml.etree.ElementTree as ET


def get_tables_by_category(
    category_name: str
):
    """
    Retrieves table schemas for all tables belonging to a specified category from an XML file.

    Args:
        xml_file_path (str): Path to the XML file containing categorized tables.
        category_name (str): The category name to filter tables by.

    Returns:
        str: XML string containing tables and their schemas for the specified category.
    """

    # Load the XML file
    xml_tree = ET.parse('./data/category_table_map.xml')
    xml_root = xml_tree.getroot()

    # Find the category element
    category_element = xml_root.find(f"./Category[@name='{category_name}']")
    if category_element is None:
        raise ValueError(
            f"Category '{category_name}' not found in the XML file.")

    # Prepare the XML string for the tables in the category
    tables_element = category_element.find('Tables')
    if tables_element is None:
        return f"No tables found for category '{category_name}'."

    # Convert the element tree to a string
    tables_xml_string = ET.tostring(
        category_element, encoding='utf-8', xml_declaration=True).decode('utf-8')

    return tables_xml_string
