import requests
import json
import os
import urllib.parse
from colorama import *
from datetime import datetime
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
            'Pragma': 'no-cache',
            'Referer': 'https://prod.snapster.bot/',
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
        url = f'https://prod.snapster.bot/api/user/getUserByTelegramId?telegramId={telegram_id}'
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        })

        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=self.headers)
                response.raise_for_status()
                result = response.json()
                if "Successfully fetched User" in response.text:
                    return result['data']
                else:
                    return None
            except (requests.exceptions.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying [{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    self.log(
                        f"{Fore.RED + Style.BRIGHT}Failed to fetch user after {retries} attempts.{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} Reason: {str(e)}{Style.RESET_ALL}"
                    )
                    return None

        self.log(
            f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} after {retries} attempts {Style.RESET_ALL}"
        )
        return None
        
    def claim_daily(self, telegram_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/dailyQuest/startDailyBonusQuest'
        data = json.dumps({ 'telegramId': telegram_id })
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if response.status_code == 200:
                    if result["result"]:
                        return result["data"]
                    else:
                        return None
                else:
                    return None
            except (requests.exceptions.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying [{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None

        self.log(
            f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} after {retries} attempts {Style.RESET_ALL}"
        )
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
                result = response.json()
                if "Successfully fetched Leagues" in response.text:
                    return result['data']
                else:
                    return None
            except (requests.exceptions.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying [{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None

        self.log(
            f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} after {retries} attempts {Style.RESET_ALL}"
        )
        return None
        
    def claim_league(self, telegram_id: str, league_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/user/claimLeagueBonus'
        data = json.dumps({ 'telegramId': telegram_id, 'leagueId': league_id })
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if response.status_code == 200:
                    if result["result"]:
                        return result["data"]
                    else:
                        return None
                else:
                    return None
            except (requests.exceptions.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying [{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None

        self.log(
            f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} after {retries} attempts {Style.RESET_ALL}"
        )
        return None
        
    def claim_referral(self, telegram_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/referral/claimReferralPoints'
        data = json.dumps({ 'telegramId': telegram_id })
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if "Successfully claimed Referral points" in response.text:
                    return result['data']
                else:
                    return None
            except (requests.exceptions.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying [{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None

        self.log(
            f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} after {retries} attempts {Style.RESET_ALL}"
        )
        return None
        
    def claim_mining(self, telegram_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/user/claimMiningBonus'
        data = json.dumps({ 'telegramId': telegram_id })
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if "Successfully claimed Mining Bonus points" in response.text:
                    return result['data']
                else:
                    return None
            except (requests.exceptions.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying [{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None

        self.log(
            f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} after {retries} attempts {Style.RESET_ALL}"
        )
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
                result = response.json()
                if "Successfully fetched Quests for User" in response.text:
                    return result['data']
                else:
                    return None
            except (requests.exceptions.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying [{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None

        self.log(
            f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} after {retries} attempts {Style.RESET_ALL}"
        )
        return None
    
    def start_quests(self, telegram_id: str, quest_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/quest/startQuest'
        data = json.dumps({ 'telegramId': telegram_id, 'questId': quest_id })
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                response.raise_for_status()
                result = response.json()
                if response.status_code == 200:
                    if result["result"]:
                        return result["data"]
                    else:
                        return None
                else:
                    return None
            except (requests.exceptions.RequestException, ValueError) as e:
                if attempt < retries - 1:
                    print(
                        f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%x %X %Z')} ]{Style.RESET_ALL}"
                        f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                        f"{Fore.RED + Style.BRIGHT}HTTP ERROR.{Style.RESET_ALL}"
                        f"{Fore.YELLOW + Style.BRIGHT} Retrying [{attempt + 1}/{retries}]{Style.RESET_ALL}",
                        end="\r",
                        flush=True
                    )
                    time.sleep(delay)
                else:
                    return None

        self.log(
            f"{Fore.RED + Style.BRIGHT}Failed{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} after {retries} attempts {Style.RESET_ALL}"
        )
        return None
        
    def claim_quests(self, telegram_id: str, quest_id: str, query: str, retries=3, delay=2):
        url = 'https://prod.snapster.bot/api/quest/claimQuestBonus'
        data = json.dumps({ 'telegramId': telegram_id, 'questId': quest_id })
        self.headers.update({ 
            'Content-Type': 'application/json',
            'Telegram-Data': query 
        })

        response = self.session.post(url, headers=self.headers, data=data)
        response.raise_for_status()
        result = response.json()
        if result["result"]:
            return result["data"]
        elif result["message"]:
            self.log(f"{Fore.YELLOW + Style.BRIGHT}[ Quest ] Already Claimed - Bug Reason{Style.RESET_ALL}")
            return None
        else:
            self.log(f"{Fore.RED + Style.BRIGHT}[ Quest ] Failed to Claim Quest Rewards{Style.RESET_ALL}")
            return None
    
    def process_query(self, query: str):

        telegram_id = str(self.load_data(query))
        if not telegram_id:
            self.log(f"{Fore.RED + Style.BRIGHT}Login failed. No TG ID received.{Style.RESET_ALL}")
            return None

        user = self.get_user(telegram_id, query)

        if user:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['username']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}[ Points{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['pointsCount']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}[ League{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {user['currentLeague']['title']} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )

            claim_daily = self.claim_daily(telegram_id, query)
            if claim_daily:
                self.log(
                    f"{Fore.GREEN+Style.BRIGHT}[ Check-in{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} {claim_daily['pointsClaimed']} {Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT}Points Claimed ]{Style.RESET_ALL}"
                )
            else:
                self.log(f"{Fore.YELLOW+Style.BRIGHT}[ Already Check-in Today ]{Style.RESET_ALL}")

            get_leagues = self.get_leagues(telegram_id, query)
            if get_leagues:
                league_ids = [league['leagueId'] for league in get_leagues if league['status'] in ['CURRENT', 'UNCLAIMED']]
                
                if league_ids:
                    league_id = league_ids[0]

                    league_bonus = self.claim_league(telegram_id, league_id, query)
                    if league_bonus:
                        self.log(
                            f"{Fore.GREEN+Style.BRIGHT}[ League Bonus{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {league_bonus['pointsClaimed']} {Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT}Points Claimed ]{Style.RESET_ALL}"
                        )
                    else:
                        next_league = next((league for league in get_leagues if league['leagueId'] == league_id + 1), None)
                        if next_league:
                            required_points = next_league['requiredNumberOfPointsToAchieve']
                            current_points = user['pointsCount']
                            less_points = required_points - current_points

                            self.log(
                                f"{Fore.YELLOW+Style.BRIGHT}[ No Available League Bonus{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} - {Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT}Less Than{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {less_points} {Style.RESET_ALL}"
                                f"{Fore.YELLOW+Style.BRIGHT}Points ]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(f"{Fore.RED+Style.BRIGHT}[ No Next League Found ]")
                else:
                    self.log(f"{Fore.RED+Style.BRIGHT}[ No CURRENT or UNCLAIMED League Id Found ]")
            else:
                self.log(f"{Fore.RED+Style.BRIGHT}[ Failed to Fetch Get Leagues Response ]")

            claim_referral = self.claim_referral(telegram_id, query)
            if claim_referral:
                if claim_referral['pointsClaimed'] > 0:
                    self.log(
                        f"{Fore.GREEN+Style.BRIGHT}[ Refferal{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {claim_referral['pointsClaimed']} {Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT}Points Claimed ]{Style.RESET_ALL}"
                    )
                else:
                    self.log(f"{Fore.YELLOW+Style.BRIGHT}[ No Available Refferal Points ]")
            else:
                self.log(f"{Fore.RED+Style.BRIGHT}[ Failed to Fetch Claim Refferal Response ]")

            claim_mining = self.claim_mining(telegram_id, query)
            if claim_mining:
                if claim_mining['pointsClaimed'] > 0:
                    self.log(
                        f"{Fore.GREEN+Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {claim_mining['pointsClaimed']} {Style.RESET_ALL}"
                        f"{Fore.GREEN+Style.BRIGHT}Points Claimed ]{Style.RESET_ALL}"
                    )
                else:
                    self.log(f"{Fore.YELLOW+Style.BRIGHT}[ No Available Mining Points ]")
            else:
                self.log(f"{Fore.RED+Style.BRIGHT}[ Failed to Fetch Claim Mining Response ]")

            get_quests = self.get_quests(telegram_id, query)
            if get_quests:
                pending_quests = []
        
                for quest in get_quests:
                    quest_id = quest['questId']
                    title = quest['title']
                    status = quest['status']

                    if status in ["EARN", "UNCLAIMED"]: 
                        pending_quests.append((quest_id, title, status))

                if not pending_quests:
                    self.log(f"{Fore.GREEN + Style.BRIGHT}[ Quest ] All tasks completed{Style.RESET_ALL}")
                else:
                    for quest_id, title, status in pending_quests:
                        if status == "EARN":
                            status_task = f"{Fore.BLUE + Style.BRIGHT}{status}{Style.RESET_ALL}"
                        elif status == "UNCLAIMED":
                            status_task = f"{Fore.YELLOW + Style.BRIGHT}{status}{Style.RESET_ALL}"
                        else:
                            status_task = f"{Fore.GREEN + Style.BRIGHT}{status}{Style.RESET_ALL}"

                        self.log(
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Quest ]{Style.RESET_ALL} "
                            f"{Fore.WHITE + Style.BRIGHT}{title}{Style.RESET_ALL}"
                            f"{Fore.BLUE + Style.BRIGHT} | {Style.RESET_ALL}"
                            f"{Fore.MAGENTA + Style.BRIGHT}[ Status ] {Style.RESET_ALL}"
                            f"{status_task}"
                        )

                        if status == "EARN":
                            start_quests = self.start_quests(telegram_id, quest_id, query)
                            if start_quests:
                                self.log(
                                    f"{Fore.GREEN + Style.BRIGHT}[ Quest ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Completed{Style.RESET_ALL}"
                                )
                            
                                claim_quests = self.claim_quests(telegram_id, quest_id, query)
                                if claim_quests:
                                    self.log(
                                        f"{Fore.GREEN + Style.BRIGHT}[ Quest ]{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}claimed{Style.RESET_ALL}"
                                        f"{Fore.BLUE + Style.BRIGHT} | {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}[ Reward ]{Style.RESET_ALL}"
                                        f"{Fore.WHITE + Style.BRIGHT} {claim_quests['pointsClaimed']} {Style.RESET_ALL}"
                                        f"{Fore.GREEN + Style.BRIGHT}Points{Style.RESET_ALL}"
                                    )
                                else:
                                    self.log(f"{Fore.RED + Style.BRIGHT}[ Quest ] Failed to Claim Quest Rewards{Style.RESET_ALL}")
                            else:
                                self.log(f"{Fore.RED + Style.BRIGHT}[ Quest ] Failed to Complete{Style.RESET_ALL}")
                    
                        elif status == "UNCLAIMED":
                            claim_quests = self.claim_quests(telegram_id, quest_id, query)
                            if claim_quests:
                                self.log(
                                    f"{Fore.GREEN + Style.BRIGHT}[ Quest ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {title} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}claimed{Style.RESET_ALL}"
                                    f"{Fore.BLUE + Style.BRIGHT} | {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}[ Reward ]{Style.RESET_ALL}"
                                    f"{Fore.WHITE + Style.BRIGHT} {claim_quests['pointsClaimed']} {Style.RESET_ALL}"
                                    f"{Fore.GREEN + Style.BRIGHT}Points{Style.RESET_ALL}"
                                )
                        else:
                            None
            else:
                self.log(f"{Fore.RED+Style.BRIGHT}[ Failed to Fetch Get Quests Response ]")

        else:
            self.log(
                f"{Fore.RED+Style.BRIGHT}[ Failed to Process Account ID"
                f"{Fore.WHITE+Style.BRIGHT} {telegram_id} "
                f"{Fore.RED+Style.BRIGHT}]"
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
                self.log(f"{Fore.CYAN + Style.BRIGHT}-------------------------------------------------------------------------{Style.RESET_ALL}")

                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-------------------------------------------------------------------------{Style.RESET_ALL}")

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
