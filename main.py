from lasagnamail import LasagnaMail
import requests
import binascii
import hashlib
import random
import string
import uuid
import os


class Hashes:
    # honestly i'm pretty sure stag is a md4 hash and not a md5, but md4 won't work so I did md5.
    def stag(username: str):
        data = f"{username}-{len(username)}-eucalyptus"
        stag = hashlib.new("md5", data.encode("utf-8")).hexdigest()
        return stag


class GuildedServer:
    def __init__(this, invite: str, cookie: str):
        this.session = requests.Session()
        this.session.headers.update(
            {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Content-Length": "18",
                "Content-Type": "application/json",
                "Cookie": f"hmac_signed_session={cookie}",
                "guilded-client-id": str(uuid.uuid4()),
                "guilded-viewer-platform": "desktop",
                "Host": "www.guilded.gg",
                "Origin": "https://www.guilded.gg",
                "Referer": f"https://www.guilded.gg/i/{invite}",
                "sec-ch-ua": '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
                "X-Requested-With": "XMLHttpRequest",
            }
        )

        this.payload = {"type": '"consume"'}
        this.url = f"https://www.guilded.gg/api/invites/{invite}"

    def join(this):
        return this.session.put(this.url, headers=this.headers, json=this.payload)


class GuildedRegister:
    def __init__(this):
        this.url = "https://www.guilded.gg/api/users?type=email"
        this.client = LasagnaMail()
        this.session = requests.Session()
        this.session.headers.update(
            {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-encoding": "gzip, deflate, br",
                "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                "content-type": "application/json",
                "cookie": "",
                "guilded-client-id": str(uuid.uuid4()),
                "guilded-stag": "unset",
                "origin": "https://www.guilded.gg",
                "referer": "https://google.com/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "sec-gpc": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
            }
        )

    def register(this):
        while True:
            username = "ecriminals_" + "".join(
                random.choices(
                    string.ascii_lowercase + string.ascii_uppercase + string.digits,
                    k=4,
                )
            )
            payload = {
                "email": this.client.createAddress(),
                "extraInfo": {"platform": "desktop"},
                "fullName": "ecriminals",
                "name": f"{username}",
                "password": "ecriminals123##~~",
            }
            this.session.headers["guilded-stag"] = Hashes.stag(username)
            return this.session.post(this.url, json=payload)


if __name__ == "__main__":
    for _ in range(500):
        _register = GuildedRegister().register()
        try:
            _name = _register.json()["user"]["name"]
            _email = _register.json()["user"]["email"]
            if "hmac_signed_session" in _register.cookies:
                _hmac = _register.cookies["hmac_signed_session"]
                print(f"Username: {_name}\nEmail: {_email}\nHmac: {_hmac}")
                open("./data/hmac.txt", "a").write(f"{_name}:{_hmac}\n")
            else:
                print(f"Username: {_name}\nEmail: {_email}\nHmac: None")
        except:
            pass
