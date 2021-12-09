import copy
from notion_update import Update
from notion_create import Create
from notion_delete import Delete
from notion import Notion
import gcs


class CRUD:
    def __init__(self, current_card_metadata):
        self.current_card_metadata = current_card_metadata
        self.previous_card_metadata = self.get_previous_card_metadata()
        self.current_card_metadata_copy = copy.deepcopy(self.current_card_metadata)
        self.previous_card_metadata_copy = copy.deepcopy(self.previous_card_metadata)

        self.final_card_metadata = {}

        self.notionAPI = Notion()

    @staticmethod
    def get_previous_card_metadata():
        return gcs.read()

    def save_current_card_metadata(self):
        return gcs.save(self.final_card_metadata)

    def get_updates(self):
        u = Update(self.current_card_metadata_copy, self.previous_card_metadata_copy)
        l_updates = u.main()

        for page_id in l_updates:
            self.notionAPI.update_page_in_database(page_id=page_id, properties=l_updates[page_id])
        self.final_card_metadata.update(u.card_metadata_update)
        self.current_card_metadata_copy = copy.deepcopy(u.current_cards)
        self.previous_card_metadata_copy = copy.deepcopy(u.previous_cards)

    def get_creates(self):
        c = Create(self.current_card_metadata_copy, self.previous_card_metadata_copy)
        l_creates = c.main()

        for card_id in l_creates:
            card = l_creates[card_id]
            res = self.notionAPI.add_page_to_database(card)

            metadata = c.card_metadata_create[card_id]
            metadata['page_id'] = res['id']
            self.final_card_metadata[card_id] = metadata

        self.current_card_metadata_copy = copy.deepcopy(c.current_cards)

    def get_deletes(self):
        d = Delete(self.current_card_metadata_copy, self.previous_card_metadata_copy)
        l_deletes = d.main()

        for page_id in l_deletes:
            self.notionAPI.delete_page_in_database(page_id=page_id)

    def main(self):
        self.get_updates()
        self.get_creates()
        self.get_deletes()
        self.save_current_card_metadata()



