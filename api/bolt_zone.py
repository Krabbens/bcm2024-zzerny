import requests

class Bolt:
    def __init__(self):
        self.url = "https://user.live.boltsvc.net/rental/cityArea/listByTile?tile_id=206%2C573&last_known_tile_version=20%3A1704811992%3A6947306752002353ff6404b76b936d72%3Ace29ad8fe1c0c01db44f4c46d304cdb8&version=CA.97.1&deviceId=8c3e8f25-e1d7-4ea8-81c6-cf80d58eb1f7&device_name=XiaomiM2101K9AG&device_os_version=12&channel=googleplay&deviceType=android&signup_session_id=2ef261b41127306e297dc19780e32506f019f97d68d21bcc5b682bd330687be6&country=pl&language=en&gps_lat=54.354711&gps_lng=18.591989&gps_accuracy_m=56.988&gps_age=46&user_id=92153560&session_id=92153560u1704892259654&distinct_id=client-92153560&rh_session_id=8c3e8f25-e1d7-4ea8-81c6-cf80d58eb1f7u1704892224"

        self.headers = {
            "User-Agent": "okhttp/4.11.0",
            "Accept-Language": "en-US",
            "Accept": "application/json",
            "Host": "user.live.boltsvc.net",
            "Authorization": "Basic KzQ4NjY3ODIyODI0OjVkMGQ0YTZmLTkxNTktNGFiNC05NDAyLWMzMzkwY2NmNmI2NA=="
        }

    def get_zones(self):
        response = requests.get(self.url, headers=self.headers)
        return response.content
    
bolt = Bolt()
print(bolt.get_zones())