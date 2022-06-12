import requests


class KakaoUserInfoFetcher:
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    def fetch(self, token: str):
        user_info = requests.get(url=self.KAKAO_USER_INFO_URL, headers={"Authorization": f"Bearer {token}"})
        return user_info.json()
