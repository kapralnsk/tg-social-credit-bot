from base_handler import BaseHandler


class PenisHandler(BaseHandler):
    @staticmethod
    def draw_penis(score):
        return f'8{"=" * (score // 100)}D'

    def get_chat_penises(self):
        profiles = self.chat.get_profiles(order_by=('-current_score',))
        profile_infos = []
        for profile in profiles:
            penis = self.draw_penis(profile.current_score)
            profile_infos.append(
                f'{penis} (@{profile.tg_username})' if profile.tg_username
                else f'{penis} ({profile.tg_full_name})'
            )
        self.send_system(
            'Current Social Credit penises are:\n{profile_infos}',
            str_format={'profile_infos': '\n'.join(profile_infos)},
        )
