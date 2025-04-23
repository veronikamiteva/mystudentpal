import pandas as pd

def load_page_data(data_manager, page_name: str, default=pd.DataFrame()):
    key      = f"{page_name}_df"
    filename = f"{page_name}.csv"
    return data_manager.load_user_data(
        session_state_key=key,
        file_name=filename,
        initial_value=default
    )