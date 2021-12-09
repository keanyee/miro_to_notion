import copy


class Update:
    def __init__(self, current_card_metadata, previous_card_metadata):
        self.current_cards = current_card_metadata
        self.previous_cards = previous_card_metadata
        self.card_metadata_update = {}

    @staticmethod
    def is_new_title(current_card_version, previous_card_version) -> bool:
        return current_card_version['title'] != previous_card_version['title']

    @staticmethod
    def is_new_description(current_card_version, previous_card_version) -> bool:
        return current_card_version['description'] != previous_card_version['description']

    @staticmethod
    def is_new_theme(current_card_version, previous_card_version) -> bool:
        return current_card_version['theme'] != previous_card_version['theme']

    @staticmethod
    def are_new_tags(current_card_version, previous_card_version) -> bool:
        current_card_version_tags = set()
        previous_card_version_tags = set()
        for tag in current_card_version['tags']:
            current_card_version_tags.add(tag['title'])
        for tag in previous_card_version['tags']:
            previous_card_version_tags.add(tag['title'])
        return len(current_card_version_tags) != len(previous_card_version_tags) or \
            len(current_card_version_tags - previous_card_version_tags) > 0

    def check_for_updates(self, current_card_version, previous_card_version) -> dict:
        update = {}
        if self.is_new_title(current_card_version, previous_card_version):
            update['title'] = {
                'type': 'title',
                'title': [{'type': 'text', 'text': {'content': current_card_version['title']}}]
            }
        if self.is_new_description(current_card_version, previous_card_version):
            update['description'] = {
                'type': 'rich_text',
                'rich_text': [{"type": "text", "text": {"content": current_card_version['description']}}]
            }
        if self.is_new_theme(current_card_version, previous_card_version):
            update['theme'] = {
                'type': 'select',
                'select': {'content': current_card_version['title']}
            }
        if self.are_new_tags(current_card_version, previous_card_version):
            update['sub-themes'] = {
                'type': 'multi_select',
                'multi_select': [{'name': tag['title']} for tag in current_card_version['tags']]
            }
        return update

    @staticmethod
    def create_metadata(card, page_id):
        metadata = copy.deepcopy(card)
        metadata['page_id'] = page_id
        return metadata

    def main(self) -> dict:
        l_updates = {}  # page_id : {'title': {}, 'description': {}, 'theme': {}}
        current_cards = copy.deepcopy(self.current_cards)
        previous_cards = copy.deepcopy(self.previous_cards)

        for card_id in self.current_cards:
            if card_id in self.previous_cards:
                current_card_version = self.current_cards[card_id]
                previous_card_version = self.previous_cards[card_id]
                updates = self.check_for_updates(current_card_version, previous_card_version)

                if updates:
                    l_updates[previous_card_version['page_id']] = updates

                metadata = self.create_metadata(current_card_version, page_id=previous_card_version['page_id'])
                self.card_metadata_update[card_id] = metadata
                current_cards.pop(card_id)
                previous_cards.pop(card_id)

        self.current_cards = current_cards
        self.previous_cards = previous_cards
        return l_updates
