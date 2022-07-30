from linkedin_api import Linkedin
import pandas as pd
from utils import utils
import json


def get_linkedin_profile_data(row):
    user_id = row[0]
    print(user_id)
    try:
        data = api.get_profile(user_id)
        print(data)

        # Get connection details
        # conn_data = api.get_profile_contact_info(user_id)
        # print(conn_data)

        if utils.is_student(data):
            """To be implemented"""
            pass
        else:
            return pd.Series(utils.extract_relevant_data(data, utils.relevant_fields, user_id))
    except Exception as e:
        print("Error fetching profile details: {}".format(e))
        return pd.Series([None]*8)


if __name__ == '__main__':
    df = pd.read_csv("data/linkedin_username.csv")
    credentials = json.load(open('secret.json'))
    api = Linkedin(credentials["username"], credentials["password"])

    df_out = df.apply(get_linkedin_profile_data, axis=1)

    df_out.columns = ["Name", "Batch", "Headline", "Experiance_1", "Experiance_2", "Experiance_3", "Skills", "Locations"]
    df_out.to_csv("data/linkedin_profile_details.csv", index=False)
