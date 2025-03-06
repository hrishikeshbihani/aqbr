import xml.etree.ElementTree as ET
tree = ET.parse('./combined_tables_updated.xml')
root = tree.getroot()

def select_dimension(user_input,selected_metric,selected_table,product_description):
    selected_table_xml= root.find(f".//table[@name='{selected_table}']")
    if selected_table_xml is not None:
    # Convert the table element to a string
        selected_table_xml = ET.tostring(selected_table_xml, encoding='unicode')
    with open('prompts/select_dimension.txt', 'r') as file:
        system_text = file.read()
    system_text=system_text.format(selected_metric=selected_metric,table_schema=selected_table_xml,product_description=product_description)
    user_text = """<question> {user_input} </question> """.format(user_input=user_input,selected_metric=selected_metric,table_schema=selected_table_xml)
    return system_text, user_text ,selected_table_xml
