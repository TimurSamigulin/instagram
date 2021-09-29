import requests
import logging

class Instagram:

    def get_user_insta_info(self, user_tag: str) -> dict:
        if not user_tag:
            logger.info(f'в user_tag была передана пустая строка')

        data = self.__get_profile_info(user_tag)
        if not data:
            logger.info(f'Пользователя {user_tag} не существует')
            return {}

        prep_data = self.__preprocess_insta_info(data)
        return prep_data


    def __get_profile_info(self, user_tag: str):
        url = f'https://www.instagram.com/{user_tag}/channel/?__a=1'
        headers = {'User-Agent': 'Mozilla'}
        req = requests.get(url, headers=headers)
        data = req.json()

        return data

    def __preprocess_insta_info(self, data: dict) -> dict:
        data = data['graphql']['user']
        user_data = self.__get_profile_data(data)

        edge_video = self.__get_edge_video(data['edge_felix_video_timeline']['edges'])
        user_data['edge_video'] = edge_video

        edge_media = self.__get_edge_media(data['edge_owner_to_timeline_media']['edges'])
        user_data['edge_media'] = edge_media

        return user_data

    def __get_profile_data(self, data):
        insta_info = {}
        insta_info['biography'] = data['biography']
        insta_info['followed_count'] = data['edge_followed_by']['count']
        insta_info['follow_count'] = data['edge_follow']['count']
        insta_info['full_name'] = data['full_name']
        insta_info['id'] = data['id']
        insta_info['is_business_account'] = data['is_business_account']
        insta_info['category_name'] = data['category_name']
        insta_info['is_private'] = data['is_private']
        insta_info['profile_pic_url'] = data['profile_pic_url']
        insta_info['insta_tag'] = data['username']
        return insta_info

    def __get_edge_video(self, edge_video):
        edge_video_timeline = []
        for edge in edge_video:
            video_timeline = {}
            media = edge['node']
            video_timeline['display_url'] = media['display_url']
            video_timeline['height'] = media['dimensions']['height']
            video_timeline['width'] = media['dimensions']['width']
            video_timeline['is_video'] = media['is_video']
            video_timeline['video_url'] = media['video_url']
            video_timeline['video_view_count'] = media['video_view_count']
            video_timeline['comment_count'] = media['edge_media_to_comment']['count']
            video_timeline['like_count'] = media['edge_liked_by']['count']
            video_timeline['title'] = media['title']
            video_timeline['video_duration'] = media['video_duration']
            edge_video_timeline.append(video_timeline)

        return edge_video_timeline

    def __get_edge_media(self, edge_timeline):
        edges_media = []

        for edge in edge_timeline:
            timeline = {}
            media = edge['node']
            timeline['display_url'] = media['display_url']
            timeline['height'] = media['dimensions']['height']
            timeline['width'] = media['dimensions']['width']
            timeline['is_video'] = media['is_video']
            if media['is_video']:
                timeline['video_url'] = media['video_url']
                timeline['video_view_count'] = media['video_view_count']
            else:
                timeline['video_url'] = None
                timeline['video_view_count'] = None
            timeline['caption'] = media.get('accessibility_caption', None)

            if media.get('edge_media_to_caption', False):
                timeline['text'] = media['edge_media_to_caption']['edges'][0]['node']['text']
            else:
                timeline['text'] = None

            if media.get('edge_media_to_comment', False):
                timeline['comment_count'] = media['edge_media_to_comment']['count']
            else:
                timeline['comment_count'] = None

            if media.get('edge_liked_by', False):
                timeline['like_count'] = media['edge_liked_by']['count']
            else:
                timeline['like_count'] = None

            if media.get('location', False):
                timeline['location'] = media['location']['name']
            else:
                timeline['location'] = None

            if media.get('edge_sidecar_to_children', False):
                carusel = self.__get_edge_media(media['edge_sidecar_to_children']['edges'])
                timeline['carusel'] = carusel
            else:
                timeline['carusel'] = None
            edges_media.append(timeline)

        return edges_media


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)s %(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)

    insta = Instagram()
    data = insta.get_user_insta_info('stride_up')
    for key, index in data.items():
        print(f'{key} - {index}')

    for media in data['edge_media']:
        print(media)