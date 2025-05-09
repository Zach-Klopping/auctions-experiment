import pandas as pd
from openpyxl import load_workbook
import os
file = open("all_apps_wide-2025-05-08 (1).csv", "r")
df = pd.read_csv("all_apps_wide-2025-05-08 (1).csv")
df.drop(columns=['participant._is_bot', 'participant.id_in_session', 'session.mturk_HITId', 'session.mturk_HITGroupId', 'session.comment', 
                 'participant._index_in_pages', 'session.code', 'session.label', 'session.is_demo', 'participant._current_app_name', 'participant.visited',
                 'participant._current_page_name', 'session.config.participation_fee', 'participant.payoff', 'stage_1.1.subsession.round_number',
                 'participant.mturk_worker_id', 'participant.mturk_assignment_id', 'participant.label', 'stage_1.1.group.id_in_subsession',
                 'stage_1.1.player.role', 'stage_1.1.player.payoff', 'session.config.real_world_currency_per_point', 'participant._max_page_index', 
                 ], inplace=True)
filename = 'my_table.xlsx'
df.to_excel(filename, index=False)
wb = load_workbook(filename)
ws = wb.active

# Set column widths
for col in ws.columns:
    max_length = 0
    col_letter = col[0].column_letter
    for cell in col:
        try:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        except:
            pass
    ws.column_dimensions[col_letter].width = max_length + 2


# Save the changes
wb.save(filename)
