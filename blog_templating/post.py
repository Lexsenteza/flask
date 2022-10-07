class Post:

    def __init__(self, data: list, id_number: int):
        self.page_number = id_number
        self.data = data

    def get_body(self):
        data_to_send = {}
        for pages in self.data:
            if pages["id"] == self.page_number:
                data_to_send["title"] = pages["title"]
                data_to_send["subtitle"] = pages["subtitle"]
                data_to_send["body"] = pages["body"]
        return data_to_send



