import copy


class CurrentMetadata:
    def __init__(self, miro_board_data):
        self.miro_board_data = miro_board_data
        self.current_frames = self.get_all_frames()
        self.current_frame_metadata = self.get_frame_metadata()
        self.current_card_metadata = self.get_card_metadata()

    def get_all_frames(self):
        frames = []
        for widget in self.miro_board_data:
            if widget['type'] == 'FRAME':
                frames.append(widget)
        return frames

    def get_frame_metadata(self):
        d = {}
        for frame in self.current_frames:
            if 'childrenIds' in frame and len(frame['childrenIds']) > 0:
                for child in frame['childrenIds']:
                    d[child] = frame['title']
        return d

    def get_card_metadata(self):
        cards = {}
        for widget in self.miro_board_data:
            if widget['type'] == 'CARD':
                card_id = widget['id']
                if self.is_card_within_frame(card_id):
                    metadata = copy.deepcopy(widget)
                    metadata['theme'] = self.get_card_theme(card_id)
                    metadata['title'] = self.clean_text(metadata['title'])
                    metadata['description'] = self.clean_text(metadata['description'])
                    cards[card_id] = metadata
        return cards

    def is_card_within_frame(self, card_id: str) -> bool:
        return card_id in self.current_frame_metadata

    def get_card_theme(self, card_id: str):
        return self.current_frame_metadata[card_id]

    @staticmethod
    def clean_text(text):
        return text.replace('<p>', '').replace('</p>', '').replace('<br />', '').replace('<br>', '')
