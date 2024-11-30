from appwrite.client import Client
from appwrite.exception import AppwriteException
from appwrite.query import Query
from appwrite.services.databases import Databases
import os

def throw_if_missing(obj: object, keys: list[str]) -> None:
    missing = [key for key in keys if key not in obj or not obj[key]]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

# This Appwrite function will be executed every time your function is triggered
def main(context):
    client = (
        Client()
        .set_endpoint(os.environ["APPWRITE_FUNCTION_API_ENDPOINT"])
        .set_project(os.environ["APPWRITE_FUNCTION_PROJECT_ID"])
        .set_key(context.req.headers["x-appwrite-key"])
    )
    databases = Databases(client)

    try:
        throw_if_missing(context.req.body, ["user_id"])
        user_id = context.req.body["user_id"]
        answer = databases.list_documents(
            database_id=os.environ["APPWRITE_DATABASE_ID"],
            collection_id=os.environ["APPWRITE_ANSWERS_COLLECTION_ID"],
            queries=[Query.equal('user_id',[user_id])],
        )

        if answer['total'] == 0:
            raise ValueError(f"Answer not found for user {user_id}!")
        elif answer['total'] > 1:
            raise ValueError(f"Too much answers found for user {user_id}! Investigate database!")


        hobbies_res = databases.list_documents(
            database_id=os.environ["APPWRITE_DATABASE_ID"],
            collection_id=os.environ["APPWRITE_HOBBIES_COLLECTION_ID"]
        )

        hobbies_res = hobbies_res["documents"]

        user = []
        for key in keys:
            user.append(answer['documents'][0][key])

        hobbies = {}
        for hobby in hobbies_res:
            hobby_val = []

            for key in keys:
                if hobby[key] is None:
                    hobby_val.append(0.5)
                if hobby[key] is True:
                    hobby_val.append(1)
                elif hobby[key] is False:
                    hobby_val.append(0)

            hobbies[hobby['name']] = hobby_val

    except AppwriteException as err:
        return context.res.json({"ok": False, "error": err.message}, 400)

    res = {
        "answers": user,
        "hobbies": hobbies
    }

    context.log(res)

    return context.res.json(
        res
    )


import numpy as np

keys = ["team_required","sport","intelectual","practical","creativity","high_budget","artistic","nature","home","much_time_on_hobby","adrenaline"]

answers={"user_id":"674b22e3925a836c1bbc","team_required":0,"sport":0.25,"intelectual":1,"practical":0.25,"creativity":0.75,"high_budget":0,"artistic":1,"nature":0.5,"home":1,"much_time_on_hobby":1,"adrenaline":0}
hobbies=[{"team_required":True,"sport":True,"intelectual":None,"practical":None,"creativity":None,"high_budget":None,"artistic":False,"nature":True,"home":False,"much_time_on_hobby":None,"adrenaline":True}]



# Example hobby data
# hobbies = {
#     "Chess": [0, 1, 1, 0, 0.5],
#     "Hiking": [1, 0, 0.5, 0.5, 1],
#     "Painting": [0, 0, 0, 1, 1]
# }
#
# # User preferences
# user = [0.25, 1, 1, 0, 0.75]
#
# # Calculate Manhattan distance for each hobby
# scores = {}
# for hobby, params in hobbies.items():
#     distance = sum(abs(u - p) for u, p in zip(user, params))
#     scores[hobby] = distance
#
# # Sort hobbies by distance (ascending order)
# sorted_hobbies = sorted(scores.items(), key=lambda x: x[1])
#
# # Output ranked hobbies
# for hobby, score in sorted_hobbies:
#     print(f"{hobby}: {score:.2f}")
