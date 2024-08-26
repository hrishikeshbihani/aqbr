import xml.etree.ElementTree as ET
tree = ET.parse('./data/table_metadata.xml')
root = tree.getroot()
tables_xml_string = ET.tostring(root, encoding='utf-8', xml_declaration=True).decode('utf-8')
def select_dimension(user_input,selected_metric,table_schema):
    with open('prompts/select_dimension.txt', 'r') as file:
        system_text = file.read()
    system_text=system_text.format(table_metadata=tables_xml_string,selected_metric=selected_metric,table_schema=table_schema)
    user_text = """<question> {user_input} </question> """.format(user_input=user_input,selected_metric=selected_metric,table_schema=table_schema)
    return system_text, user_text
