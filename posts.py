image_1 = "assets/img/cactus.jpg"
image_2 = "assets/img/bored.jpg"
image_3 = "assets/img/fasting.jpg"


class Post:

    def __init__(self, data: list, page_number: int):
        self.data = data
        self.number = page_number
        self.images = [image_1, image_2, image_3]

    def get_body(self):
        dict_to_send = {}
        for page in self.data:
            identity = page["id"]
            if identity == self.number:
                dict_to_send["body"] = page["body"]
                dict_to_send["title"] = page["title"]
                dict_to_send["subtitle"] = page["subtitle"]
                dict_to_send["path"] = self.images[identity - 1]

        return dict_to_send


