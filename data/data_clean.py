import pandas as pd
file = open("all_apps_wide-2025-05-08.csv", "r")
df = pd.read_csv("all_apps_wide-2025-05-08.csv")
df.drop(columns=['participant._is_bot', 'participant.id_in_session', 'session.mturk_HITId', 'session.mturk_HITGroupId', 'session.comment', 'participant._index_in_pages', 'session.code', 'session.label', 'session.is_demo', 'participant._current_app_name', 'participant._current_page_name', 
                 'participant.mturk_worker_id', 'participant.mturk_assignment_id', 'participant.label'], inplace=True)
pd.set_option('display.max_columns', None)
print(df)
