def select_product(user_input):
    with open('prompts/nlq_select_product.txt', 'r') as file:
        system_text = file.read()
    user_text = """<question> {user_input} </question> """.format(user_input=user_input)
    return system_text, user_text
