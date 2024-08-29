import csv
import xml.etree.ElementTree as ET


def read_csv_for_descriptions(csv_file):
    """Read the CSV file and return a dictionary with table names and column descriptions."""
    descriptions = {}
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            table_name = row['TableName']
            column_name = row['ColumnName']
            description = row['ColumnDescription']
            if table_name not in descriptions:
                descriptions[table_name] = {}
            descriptions[table_name][column_name] = description
    return descriptions


def update_metrics(table, descriptions):
    """Update metrics section of the XML table with descriptions from the dictionary."""
    metrics = table.find("metrics")
    if metrics is not None:
        csv_metric_names = set(descriptions.keys())
        # Remove columns not in CSV
        remove_unused_columns(metrics, 'metric_name', csv_metric_names)
        # Update descriptions for existing columns
        for column in metrics.findall("column"):
            metric_name = column.get("metric_name")
            if metric_name in descriptions:
                description = descriptions[metric_name]
                if description and description != "EMPTY":
                    column.set("description", description)


def update_dimensions(table, descriptions):
    """Update dimensions section of the XML table with descriptions from the dictionary."""
    dimensions = table.find("dimensions")
    if dimensions is not None:
        csv_dimension_names = set(descriptions.keys())
        # Remove columns not in CSV
        remove_unused_columns(
            dimensions, 'dimension_name', csv_dimension_names)
        # Update descriptions for existing columns
        for column in dimensions.findall("column"):
            dimension_name = column.get("dimension_name")
            if dimension_name in descriptions:
                description = descriptions[dimension_name]
                if description and description != "EMPTY":
                    column.set("description", description)


def remove_unused_columns(section, column_attribute, csv_column_names):
    """Remove columns from XML section that are not present in the CSV."""
    for column in section.findall("column"):
        column_name = column.get(column_attribute)
        if column_name not in csv_column_names:
            section.remove(column)


def update_xml_with_descriptions(xml_file, descriptions):
    """Update the XML file with column descriptions from the dictionary and remove missing columns."""
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for table in root.findall("table"):
        table_name = table.get("name")
        if table_name in descriptions:
            update_metrics(table, descriptions[table_name])
            update_dimensions(table, descriptions[table_name])

    # Save the updated XML to a new file
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)
    print(f"Updated XML data written to {xml_file}")


def main():
    csv_file = "combined_tables.csv"
    xml_file = "combined_tables.xml"

    print("Reading column descriptions from CSV...")
    descriptions = read_csv_for_descriptions(csv_file)
    print("Descriptions read from CSV:", descriptions)

    print("Updating XML file with descriptions...")
    update_xml_with_descriptions(xml_file, descriptions)

    print("XML file update completed.")


if __name__ == "__main__":
    main()
