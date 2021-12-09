import copy
import env_vars as env


class Create:
    def __init__(self, current_card_metadata, previous_card_metadata):
        self.current_cards = current_card_metadata
        self.previous_cards = previous_card_metadata
        self.card_metadata_create = {}

    @staticmethod
    def check_for_create(current_card):
        return {
            'title': {
                'type': 'title',
                'title': [{'type': 'text', 'text': {'content': current_card['title']}}]
            },
            'description': {
                'type': 'rich_text',
                'rich_text': [{'type': 'text', 'text': {'content': current_card['description']}}],
            },
            'theme': {
                'type': 'select',
                'select': {'name': current_card['theme']},
            },
            'sub-themes': {
                'type': 'multi_select',
                'multi_select': [{'name': tag['title']} for tag in current_card['tags']]
            },
            'url': {
                'type': 'url',
                'url': f'https://miro.com/app/board/{env.MIRO_BOARD_ID}/?moveToWidget={current_card["id"]}&cot=14'
            }
        }

    def main(self) -> dict:
        l_create = {}
        current_cards = copy.deepcopy(self.current_cards)
        for card_id in self.current_cards:
            if card_id not in self.previous_cards:
                card = self.current_cards[card_id]
                data = self.check_for_create(card)
                l_create[card_id] = data

                current_cards.pop(card_id)
                self.card_metadata_create[card_id] = card
        self.current_cards = current_cards
        return l_create
