import vk_api
import os
import logging

logging.basicConfig(level=logging.DEBUG)


class VK:

    def __init__(self):
        self.vk_session = vk_api.VkApi(os.environ['VK_LOGIN'], os.environ['VK_PASS'])
        self.vk_session.auth()
        self.vk = self.vk_session.get_api()

    def get_news(self):
        result = self.vk.wall.get(owner_id=-194736647)
        logging.info(result)
        return result['items']
