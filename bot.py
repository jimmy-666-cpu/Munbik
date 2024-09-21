import requests, time

class MoonBix:
    def __init__(self, token):
        self.session = requests.session()
        self.session.headers.update({
            'authority': 'www.binance.com',
            'accept': '*/*',
            'accept-language': 'en-EG,en;q=0.9,ar-EG;q=0.8,ar;q=0.7,en-GB;q=0.6,en-US;q=0.5',
            'bnc-location': '',
            'clienttype': 'web',
            'content-type': 'application/json',
            'lang': 'en',
            'origin': 'https://www.binance.com',
            'referer': 'https://www.binance.com/en/game/tg/moon-bix',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            
        })
        self.token = token
        
        self.game_response = None

    def login(self):
        json_data = {
            'queryString': self.token,
            'socialType': 'telegram',
        }

        response = self.session.post(
            'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/third-party/access/accessToken',
            json=json_data,
        )

        if response.status_code != 200:
            return False

        data = response.json()
        
        accessToken = data['data']['accessToken']

        self.session.headers['x-growth-token']= accessToken
        
        return response.status_code == 200
    
    def user_info(self):
        json_data = {
            'resourceId': 2056,
        }

        response = self.session.post(
            'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/user/user-info',
            json=json_data,
        )
        
        return response.json()
    
    def start_game(self):
        json_data = {
            'resourceId': 2056,
        }

        response = self.session.post(
            'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/start',
            json=json_data,
        )


        self.game_response = response.json()
        
        if response.json()['code'] == '000000':
            return True
        
        if response.json()['code'] == '116002':
            print(' Attempts not enough !')
        else:
            print(" ERROR ! ")
        
        return False
    
    def game_data(self):
        url = 'https://vemid42929.pythonanywhere.com/api/v1/moonbix/play'

        response = requests.post(url, json=self.game_response).json()

        if response['message']=='success':
            self.game = response['game']
            return True
        
        print(response['message'])
        return False
        

    def complete_game(self):
        
        json_data = {
            'resourceId': 2056,
            'payload': self.game['payload'],
            'log': self.game['log'],
        }

        response = self.session.post(
            'https://www.binance.com/bapi/growth/v1/friendly/growth-paas/mini-app-activity/third-party/game/complete',
            json=json_data,
        )

        return response.json()['success']

    def start(self):
        if not self.login():
            print(" Faild To Login")
            return
        print(" Done Logged in !")
        
        if not self.start_game():
            print(" Faild to start game !")
            return
        
        print(" Game Has Started !")

        sleep(45)

        if not self.game_data():
            print(" Faild to generate game data !")
            return
        
        print(" Done game data generated !")

        if not self.complete_game():
            print(" Faild to complete game")
        
        print(f" done complete game you earn + {self.game['log']}")


def sleep(sec):
    for i in range(sec, -5, -5):
        print(f' Sleeping {i} ', end='\r')
        time.sleep(5)

if __name__ == '__main__':
    while True:

        with open('tokens.txt') as f:
            tokens = f.readlines()
        
        for token in tokens:
            print('=============================')
            x = MoonBix(token.strip())
            x.start()
            print('=============================')
            sleep(15)

        sleep(60)

