from flask import Flask, request
import logging
import json
import random
from constants import Constants
from vk import VK

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route("/", methods=["POST"])
def main():
    logging.info(request.json)

    response = {
        "version": request.json["version"],
        "session": request.json["session"],
        "response": {
            "end_session": False
        }
    }

    vk = VK()

    req = request.json
    if req["session"]["new"]:
        response["response"]["text"] = Constants["hello"]
    else:
        tokens = req["request"]["nlu"]["tokens"]
        vk_news = vk.get_news()
        if req["request"]["original_utterance"] == "Открыть группу":
            response["response"]["text"] = "Приятного чтения!"
        if list(set(tokens) & {"новое", "новенькое", "новости"}):
            vk_result = vk_news[0]
        else:
            vk_keys = [element for element in vk_news
                       if list(set(tokens) & set(element["text"].lower().replace(".", " ").split(" ")))]
            logging.info(vk_keys)
            vk_result = vk_keys[random.randint(0, len(vk_keys) - 1)]
        if vk_result is not None:
            response["response"]["text"] = Constants["answers"][random.randint(0, len(Constants["answers"]) - 1)].format(vk_result["text"].split("\n")[0])
            response["response"]["buttons"] = [{"title": "Открыть группу",
                                                "url": "https://vk.com/betry_developer?w=wall-194736647_{0}"
                                                    .format(vk_result["id"])}]

    return json.dumps(response)
