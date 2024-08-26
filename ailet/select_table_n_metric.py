import xml.etree.ElementTree as ET
tree = ET.parse('./data/table_metadata.xml')
root = tree.getroot()
tables_xml_string = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
def select_table_n_metric(user_input,product_description):
    with open('prompts/select_table_n_metric.txt', 'r') as file:
        system_text = file.read()
    system_text=system_text.format(table_metadata=tables_xml_string,product_description=product_description)
    user_text = """<question> {user_input} </question> """.format(user_input=user_input,product_description=product_description)
    return system_text, user_text
