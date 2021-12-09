class Delete:
    def __init__(self, current_card_metadata, previous_card_metadata):
        self.current_cards = current_card_metadata
        self.previous_cards = previous_card_metadata

    def main(self) -> list:
        l_deletes = []
        if len(self.previous_cards) > 0:
            for card_id in self.previous_cards:
                page_id = self.previous_cards[card_id]['page_id']
                l_deletes.append(page_id)
        return l_deletes
