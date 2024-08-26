import os


def concatenate_files(keywords, output_file):
    """
    Concatenates the contents of all files whose names contain any of the given keywords using os.system and cat command.

    :param keywords: List of keywords to search for in file names.
    :param output_file: The name of the output file where the concatenated content will be saved.
    """
    keyword_patterns = ' '.join(['/Users/anubhavkumar/work/clickhouse-queries/migrations/*{}*'.format(keyword)
                                for keyword in keywords])
    os.system('cat {} > {}'.format(keyword_patterns, output_file))


concatenate_files([
    "av",
    "agent",
    "msc",
    "operatordashboard",
    "mscontroller",
    "selfvideo",
    "agentservices",
    "taskmastertask",
    "tasky",
    "tasks",
    "profile",
    "profiles",
    "capture",
    "task",
    "pg",
    "pm",
    "kyc",
    "documentfetchermanager",
    "reviewdashboard",
    "workflowmanager",
    "schedulingservice",
    "profilesmanager",
], "vs_queries.sql")
