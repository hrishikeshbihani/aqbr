def select_table_value(user_input, table_schema):
    with open('prompts/nlq_select_table.txt', 'r') as file:
        system_text_template= file.read()
    system_text=system_text_template.format(table_schema=table_schema)
    user_text = """<question> {user_input} </question> """.format(user_input=user_input)
    return system_text, user_text