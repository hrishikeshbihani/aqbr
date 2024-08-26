def check_valid_query(user_input):
    with open('prompts/nlq_check_valid_query.txt', 'r') as file:
        system_text = file.read()
    user_text = """<question> {user_input} </question> """.format(user_input=user_input)
    return system_text, user_text
