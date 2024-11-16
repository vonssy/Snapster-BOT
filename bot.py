import requests
import json
import os
import urllib.parse
import random
from colorama import *
from datetime import datetime, timedelta
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class SnapsterTradingApp:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            'Host': 'prod.snapster.bot',
            'Origin': 'https://prod.snapster.bot',
            'Pragma': 'no-cache',
            'Referer': 'https://prod.snapster.bot/main',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Snapster Trading App - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get('user', [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            telegram_id = user_data['id']
            return telegram_id
        else:
            raise ValueError("User data not found in query.")

    def get_user(self, telegram_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/user/getUserByTelegramId'
        data = json.dumps({'telegramId':telegram_id})
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        }) 

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None

    def claim_daily(self, telegram_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/dailyQuest/claimDailyQuestBonus'
        data = json.dumps({'telegramId':telegram_id})
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        }) 

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None

    def get_leagues(self, telegram_id: str, query: str, retries=3, delay=2):
        url = f'https://prod.snapster.bot/api/user/getLeagues?telegramId={telegram_id}'
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        }) 

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def claim_league(self, telegram_id: str, league_id: int, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/user/claimLeagueBonus'
        data = json.dumps({'telegramId':telegram_id, 'leagueId':league_id})
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        }) 

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def claim_refferal(self, telegram_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/referral/claimReferralPoints'
        data = json.dumps({'telegramId':telegram_id})
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        }) 

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def claim_mining(self, telegram_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/user/claimMiningBonus'
        data = json.dumps({'telegramId':telegram_id})
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        }) 

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def get_quests(self, telegram_id: str, query: str, retries=3, delay=2):
        url = f'https://prod.snapster.bot/api/quest/getQuests?telegramId={telegram_id}'
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        }) 

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def start_quests(self, telegram_id: str, quest_id: int, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/quest/startQuest'
        data = json.dumps({'telegramId':telegram_id, 'questId':quest_id})
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query
        }) 

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
        
    def claim_quests(self, telegram_id: str, quest_id: int, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/quest/claimQuestBonus'
        data = json.dumps({'telegramId':telegram_id, 'questId':quest_id})
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        }) 

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying... {Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT}[{attempt+1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None
    
    def process_query(self, query: str):

        telegram_id = str(self.load_data(query))
        if not telegram_id:
            self.log(
                f"{Fore.MAGENTA + Style.BRIGHT}[ Account ID{Style.RESET_ALL}"
                f"{Fore.WHITE + Style.BRIGHT} {telegram_id} {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}] [ Status{Style.RESET_ALL}"
                f"{Fore.RED + Style.BRIGHT} Login Failed {Style.RESET_ALL}"
                f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
            )
            return
        
        if telegram_id:
            user = self.get_user(telegram_id, query)
            if user and user['message'] == 'Successfully fetched User':
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['data']['username']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Points{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['data']['pointsCount']} $SNAPS {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}[ League{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {user['data']['currentLeague']['title']} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                )
                time.sleep(3)

                now_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
                last_checkin = user['data']['lastDailyBonusClaimDate']
                if last_checkin:
                    last_checkin_utc = datetime.strptime(last_checkin, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=pytz.utc) + timedelta(hours=24)
                else:
                    last_checkin_utc = now_utc
                    
                last_checkin_wib = last_checkin_utc.astimezone(wib).strftime('%x %X %Z')

                if now_utc >= last_checkin_utc:
                    claim_daily = self.claim_daily(telegram_id, query)
                    if claim_daily and claim_daily['message'] == 'Successfully claimed Daily Bonus points':
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Rewards{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {claim_daily['data']['pointsClaimed']} $SNAPS {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Check-In{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Is Already Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Next Claim at{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {last_checkin_wib} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(3)
                
                leagues = self.get_leagues(telegram_id, query)
                if leagues and leagues['message'] == 'Successfully fetched Leagues':
                    for i, league in enumerate(leagues['data']):
                        league_id = league['leagueId']
                        status = league['status']

                        if league and status in ['CURRENT', 'UNCLAIMED']:
                            claim_league = self.claim_league(telegram_id, league_id, query)                           
                            if claim_league and claim_league['message'] == 'Successfully claimed Referral points':
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ League Bonus{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {league['title']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Rewards{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {claim_league['data']['pointsClaimed']} $SNAPS {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            elif claim_league and claim_league['message'] == 'Not eligible for claiming bonus':
                                if i + 1 < len(leagues['data']):
                                    next_league = leagues['data'][i + 1]
                                    next_title = next_league['title']
                                    required_points = next_league['requiredNumberOfPointsToAchieve']
                                    current_points = user['data']['pointsCount']
                                    less_points = required_points - current_points

                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ League Bonus{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {next_title} {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}Not Eligible{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reason{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} -{less_points} $SNAPS {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                        f"{Fore.MAGENTA + Style.BRIGHT}[ League{Style.RESET_ALL}"
                                        f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ League Bonus{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {league['title']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            time.sleep(1)

                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ League{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(3)

                claim_refferal = self.claim_refferal(telegram_id, query)
                if claim_refferal and claim_refferal['message'] == 'Successfully claimed Referral points':
                    rewards = claim_refferal['data']['pointsClaimed']
                    if rewards > 0:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Rewards{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {rewards} $SNAPS {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} Not Available Points {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(3)
                
                claim_mining = self.claim_mining(telegram_id, query)
                if claim_mining and claim_mining['message'] == 'Successfully claimed Mining Bonus points':
                    rewards = claim_mining['data']['pointsClaimed']
                    if rewards > 0:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Is Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Rewards{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {rewards} $SNAPS {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                            f"{Fore.YELLOW+Style.BRIGHT} Not Available Points {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                        f"{Fore.RED+Style.BRIGHT} Isn't Claimed {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(3)

                quests = self.get_quests(telegram_id, query)
                if quests and quests['message'] == 'Successfully fetched Quests for User':
                    for quest in quests['data']:
                        quest_id = quest['id']
                        status = quest['status']

                        if quest and status == 'EARN':
                            start = self.start_quests(telegram_id, quest_id, query)
                            if start and start['message'] == 'Successfully started Quest earn':
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Started{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )

                                claim = self.claim_quests(telegram_id, quest_id, query)
                                if claim and claim['message'] == 'Successfully claimed Quest points':
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ] [ Rewards{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {claim['data']['pointsClaimed']} $SNAPS {Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                    )
                                elif claim and claim['message'] == 'Not possible to claim bonus for this quest':
                                    self.log(
                                        f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                        f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                        f"{Fore.YELLOW+Style.BRIGHT}Is Already Claimed{Style.RESET_ALL}"
                                        f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                    )

                            else:
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                    f"{Fore.RED+Style.BRIGHT}Isn't Started{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )

                        elif status == 'UNCLAIMED':
                            claim = self.claim_quests(telegram_id, quest_id, query)
                            if claim and claim['message'] == 'Successfully claimed Quest points':
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN+Style.BRIGHT}Is Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ] [ Rewards{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {claim['data']['pointsClaimed']} $SNAPS {Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                                )
                            elif claim and claim['message'] == 'Not possible to claim bonus for this quest':
                                self.log(
                                    f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                    f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                    f"{Fore.YELLOW+Style.BRIGHT}Is Already Claimed{Style.RESET_ALL}"
                                    f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )
                            else:
                                self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Quest{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {quest['title']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Isn't Claimed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                                )

                else:
                    self.log(
                        f"{Fore.MAGENTA + Style.BRIGHT}[ Quests{Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT} Data Is None {Style.RESET_ALL}"
                        f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                    )
            else:
                self.log(
                    f"{Fore.MAGENTA + Style.BRIGHT}[ Account ID{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} {telegram_id} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}] [ Status{Style.RESET_ALL}"
                    f"{Fore.RED + Style.BRIGHT} User Data Is None {Style.RESET_ALL}"
                    f"{Fore.MAGENTA + Style.BRIGHT}]{Style.RESET_ALL}"
                )

    def main(self):
        try:
            with open('query.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        seconds = 60
                        while seconds > 0:
                            formatted_time = self.format_seconds(seconds)
                            print(
                                f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                                f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                                end="\r"
                            )
                            time.sleep(1)
                            seconds -= 1

                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Snapster Trading App - BOT.{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    snapster = SnapsterTradingApp()
    snapster.main()
