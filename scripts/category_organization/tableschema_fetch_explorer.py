## Input

from scripts.data_lib import get_table_list, get_table_schema

product_name = "GCP"
output_file_path = "./data/gcp_queries_xml.xml"

## Script
list_of_tables = get_table_list(product_name)
list_of_table_names = list(map(lambda data: data['name'], list_of_tables))
print(list_of_table_names)
table_schema_xml = get_table_schema(list_of_table_names)
print(table_schema_xml)
open(output_file_path, "w+").write(table_schema_xml)
