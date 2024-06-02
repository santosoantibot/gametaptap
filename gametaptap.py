import requests
from requests.structures import CaseInsensitiveDict
import datetime
import time
from colorama import init, Fore, Style
init(autoreset=True)

# cuman recode punya orang bang. gwe gak jago

def informasi_user(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get('https://gateway.blum.codes/v1/user/me', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        hasil = response.json()
        if hasil['message'] == 'Token is invalid':
            print(f"{Fore.RED+Style.BRIGHT}Token salah")
            return None
        else:
            print(f"{Fore.RED+Style.BRIGHT}Gagal mendapatkan informasi user")
            return None

def saldomu_piro(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.get('https://game-domain.blum.codes/api/v1/user/balance', headers=headers)
    return response.json()


def game_jembot(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
    }
    response = requests.post('https://game-domain.blum.codes/api/v1/game/play', headers=headers)
    return response.json()

def yok_claim(token, game_id, points):
    url = "https://game-domain.blum.codes/api/v1/game/claim"

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json, text/plain, */*"
    headers["accept-language"] = "en-US,en;q=0.9"
    headers["authorization"] = "Bearer "+token
    headers["content-type"] = "application/json"
    headers["origin"] = "https://telegram.blum.codes"

    headers["priority"] = "u=1, i"
    headers["user-agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0"
    data = '{"gameId":"'+game_id+'","points":'+str(points)+'}'

    resp = requests.post(url, headers=headers, data=data)
    return resp  



def refresh_token(old_refresh_token):
    url = 'https://gateway.blum.codes/v1/auth/refresh'
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'Content-Type': 'application/json',
        'origin': 'https://telegram.blum.codes',
        'referer': 'https://telegram.blum.codes/'
    }
    data = {
        'refresh': old_refresh_token
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

with open('auth.txt', 'r') as file:
    tokens = file.read().splitlines()

def check_daily_reward(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://telegram.blum.codes',
        'content-length': '0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24", "Microsoft Edge WebView2";v="125"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site'
    }
    response = requests.post('https://game-domain.blum.codes/api/v1/daily-reward?offset=-420', headers=headers)
    return response.json() 

while True:
    for token in tokens:
        info_akun = informasi_user(token)
        if info_akun is None:
            continue
        print(f"\n{Fore.GREEN+Style.BRIGHT}+++++++++  +++++++++", end="", flush=True)

        print(f"\r{Fore.YELLOW+Style.BRIGHT}Getting Info....", end="", flush=True)

        balance_info = saldomu_piro(token)
        print(f"\r{Fore.GREEN+Style.BRIGHT} Saldo :  {balance_info['availableBalance']}", flush=True)
        print(f"{Fore.BLUE+Style.BRIGHT} *Tiket Game*: {balance_info['playPasses']}")

        farming_info = balance_info.get('farming')
        end_time_ms = farming_info['endTime']
        end_time_s = end_time_ms / 1000.0
        end_utc_date_time = datetime.datetime.fromtimestamp(end_time_s, datetime.timezone.utc)
        current_utc_time = datetime.datetime.now(datetime.timezone.utc)
        time_difference = end_utc_date_time - current_utc_time
        hours_remaining = int(time_difference.total_seconds() // 3600)
        minutes_remaining = int((time_difference.total_seconds() % 3600) // 60)
        print(f"Waktu tunggu Claim Farmingan: {hours_remaining} jam {minutes_remaining} menit")
       
        if hours_remaining < 0:


            print(f"\r{Fore.GREEN+Style.BRIGHT} started game", flush=True)
        
        if balance_info['playPasses'] > 0:
            print(f"{Fore.CYAN+Style.BRIGHT}Playing game...")
            game_response = game_jembot(token)
            print(f"\r{Fore.CYAN+Style.BRIGHT}Checking game...", end="", flush=True)
            time.sleep(1)
            claim_response = yok_claim(token, game_response['gameId'], 2000)
            if claim_response is None:
                print(f"\r{Fore.GREEN+Style.BRIGHT}lagi main tunggu..", flush=True)

            while True:
                if claim_response.text == '{"message":"game session not finished"}':
                    time.sleep(1)  
                    print(f"\r{Fore.GREEN+Style.BRIGHT}lagi main tunggu..", flush=True)
                    claim_response = yok_claim(token, game_response['gameId'], 2000)
                    if claim_response is None:
                        print(f"\r{Fore.RED+Style.BRIGHT}Gagal mengklaim game, memproses...", flush=True)

                elif claim_response.text == '{"message":"game session not found"}':
                    print(f"\r{Fore.RED+Style.BRIGHT}Game sudah berakhir", flush=True)
                    break

                else:
                    print(f"\r{Fore.YELLOW+Style.BRIGHT}Game Berhasil di selesaikan <> {claim_response.text}", flush=True)
                    break
     
       
    updated_tokens = []
    print(f"\n{Fore.GREEN+Style.BRIGHT}+++++++++{Fore.WHITE+Style.BRIGHT}akun berhasil di proses{Fore.GREEN+Style.BRIGHT}+++++++++", end="", flush=True)
    print(f"\r\n\n{Fore.GREEN+Style.BRIGHT}Refreshing token...", end="", flush=True)
    for token in tokens:
        refresh_response = refresh_token(token)

        updated_tokens.append(refresh_response['refresh'])
    print(f"\r{Fore.GREEN+Style.BRIGHT}Refresh token sukses!", flush=True)



    with open('auth.txt', 'w') as file:
        for updated_token in updated_tokens:
            file.write(updated_token + '\n')
    import sys
    import time

    waktu_tunggu = 10
    for detik in range(waktu_tunggu, 0, -1):
        sys.stdout.write(f"\r{Fore.CYAN}Menunggu waktu claim berikutnya dalam {Fore.CYAN}{Fore.WHITE}{detik // 60} menit {Fore.WHITE}{detik % 60} detik")
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write("\rWaktu claim berikutnya telah tiba!                                      \n")
