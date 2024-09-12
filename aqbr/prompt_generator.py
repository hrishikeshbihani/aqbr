def get_prompt_header_file_name(product):
    if (product == "VS"):
        return "./prompts/vs_prompt.txt"
    if (product == "EVE"):
        return "./prompts/eve_prompt.txt"


def get_sample_email_file_name(product):
    if (product == "VS"):
        return "./prompts/vs_sample_email.txt"
    if (product == "EVE"):
        return "./prompts/eve_sample_email_v2.txt"


def get_customization_prompt(custom_prompt_inputs):
    if (len(custom_prompt_inputs) > 0):
        custom_prompt_input_generated = ""
        for i in range(0, len(custom_prompt_inputs)):
            custom_prompt_input_generated = custom_prompt_input_generated + "\n" + \
                "{index}. {prompt}".format(index=i+1,
                                           prompt=custom_prompt_inputs[i])
        return """
        The above example that is given to you needs to updated with following rules.
        {custom_prompt_input_generated}
        
    """.format(custom_prompt_input_generated=custom_prompt_input_generated)
    return ""


def get_prompt_header(product):
    prompt_header_file = get_prompt_header_file_name(product)
    prompt_header = open(prompt_header_file).read()
    return prompt_header


def get_prompt_tail():
    prompt_tail = """Write an Email to my clients using the above data to explain them how they have improved/impaired in this period as compared to previous. Ensure you include every item of a metric even if you do not see any notable change in the metric. Wherever you are comparing the data, include the percentage increase/decrease.
    
    """
    return prompt_tail


def get_sample_email(product):
    sample_email_file_name = get_sample_email_file_name(product)
    sample_email = open(sample_email_file_name).read()
    return sample_email


def get_storyline_prompt(product, data_body, custom_prompt_inputs):
    prompt_header = get_prompt_header(product)
    custom_prompt = get_customization_prompt(custom_prompt_inputs)
    sample_email = get_sample_email(product)
    prompt_tail = get_prompt_tail()
    return """{prompt_header}
{prompt_body}


{prompt_tail}

I am including a sample Email below for you to refer. This is only for reference, you can alter the email structure if need be.

{sample_email}

{custom_prompt}

Keep the Email concise and give lesser explanations. Output me the final Email that I can send to my client without editting. Keep the indentation of the contents of the email correct.
""".format(prompt_body=data_body, prompt_header=prompt_header, prompt_tail=prompt_tail, sample_email=sample_email, custom_prompt=custom_prompt)
