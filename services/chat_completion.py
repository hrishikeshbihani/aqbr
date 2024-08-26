from services.openai_request import make_call_to_openai
from utils.table_category_utils import get_tables_by_category


def apply_ou_filter_in_query(query_without_filters, tables_and_columns, ou_id):
  prompt = """
  You are given a clickhouse query below:
  <Query>
    {query_without_filters}
  </Query>
  
  The query above fetches data across all organizations. You need to add appropriate filter in WHERE clauses so that output of the query includes only data that are belonging to Organization with OUID - {ou_id}.
  
  In the tables that are used in the query above, there should be a column for storing OUID.
  
  I am providing the tables schemas of the tables out of which one is used in the above query: 
  {tables_and_columns}
  
  Output only the final Query. Do not write anything else. I do not want any explanation. Do not include the tag ```sql either. Just the query as plaintext.
  """.format(query_without_filters = query_without_filters, tables_and_columns = tables_and_columns, ou_id = ou_id)
  output = make_call_to_openai(prompt)
  return output
  
def get_question_category(question):
  vs_context = open("./prompts/vs_pdt-context.txt").read()
  categories_list = open("./prompts/categories.xml").read()
  prompt = """
  **Context:**
    {vs_context}

    ---

  **Task:**

    As a product manager, I need to categorize my questions based on predefined categories. Below is the list of categories in XML format:

    - **Categories:**
      {categories_list}

  **Objective:**

    Determine which category my question falls into:
    {question}

  **Instructions:**

    - Ensure the category is one of those listed above. 
    - Only write the category name in the output, without any additional text.
    - If the question is too random or doesn't relate to the product at all, output "INDETERMINANT".

  """.format(vs_context = vs_context, categories_list = categories_list, question = question)
  output = make_call_to_openai(prompt)
  return output

def get_tables_and_columns(question, category):
  vs_context = open("./prompts/vs_pdt-context.txt").read()
  category_table_list = get_tables_by_category(category)
  prompt = """
  **Context:**
    {vs_context}

    ---

    **Task:**

    As a product manager, I need to determine which tables and columns in my product's data are likely to contain the information I need.

    - **Category of Tables:**
      {category_table_list}

    **Objective:**

    Help me identify the table and its columns that may contain the answer to the following question:
    {question}

    **Instructions:**

    - Output the table and columns that may contain the answer in XML format.
    - The XML structure should be free-form, without a fixed schema.
    - Do not include any additional text, and do not use XML tags like ```xml.
    - You may return up to TWO possibilities.

  """.format(vs_context=vs_context, category_table_list=category_table_list, question=question)
  output = make_call_to_openai(prompt)
  return output

def get_query_by_shortlisted_tables(question, possible_tables):
  vs_context = open("./prompts/vs_pdt-context.txt").read()
  prompt = """
  **Context:**
    {vs_context}

    ---

    **Task:**

    As a product manager, I need to query my product's data using ClickHouse. Below is the relevant table schema:

    - **Tables and Columns:**
      {possible_tables}

    **Objective:**

    I need a ClickHouse query to answer the following question:
    {question}

    **Instructions:**

    - Use the provided table and column information to craft the query.
    - Select only one table unless absolutely confident that multiple tables are necessary to derive the correct answer.
    - Ensure the query is accurate and aligns with the schema provided.

  """.format(vs_context = vs_context, question = question, possible_tables = possible_tables)
  output = make_call_to_openai(prompt)
  return output

def get_query(question, ou_id):
  question_category = get_question_category(question)
  tables_and_columns = get_tables_and_columns(question, question_category)
  query_without_filters = get_query_by_shortlisted_tables(
      question, tables_and_columns)
  query_with_ou_filters = apply_ou_filter_in_query(
      query_without_filters, tables_and_columns, ou_id)
  return query_with_ou_filters
