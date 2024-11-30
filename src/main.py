import appwrite
from appwrite.client import Client
from appwrite.query import Query
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
import os

def throw_if_missing(obj: object, keys: list[str]) -> None:
    """
    Throws an error if any of the keys are missing from the object

    Parameters:
        obj (object): Object to check
        keys (list[str]): List of keys to check

    Raises:
        ValueError: If any keys are missing
    """
    missing = [key for key in keys if key not in obj or not obj[key]]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")

# This Appwrite function will be executed every time your function is triggered
def main(context):

    throw_if_missing(os.environ, ["APPWRITE_DATABASE_ID", "APPWRITE_ANSWERS_COLLECTION_ID", "APPWRITE_HOBBIES_COLLECTION_ID"])

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
            database_id=context.req.body["APPWRITE_DATABASE_ID"],
            collection_id=context.req.body["APPWRITE_ANSWERS_COLLECTION_ID"],
            queries=[Query.equal('user_id',[user_id])],
        )

        if len(answer) == 0:
            raise ValueError(f"Answer not found for user {user_id}!")
        elif len(answer) > 1:
            raise ValueError(f"Too much answers found for user {user_id}! Investigate database!")

        hobbies_res = databases.list_documents(
            database_id=context.req.body["APPWRITE_DATABASE_ID"],
            collection_id=context.req.body["APPWRITE_HOBBIES_COLLECTION_ID"]
        )
    except ValueError as err:
        return context.res.json({"ok": False, "error": err.message}, 400)



    return context.res.json(
        {
            "answers": answer,
            "hobbies": hobbies_res
        }
    )

import numpy as np

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
