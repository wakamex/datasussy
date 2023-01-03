import json
import requests
import pandas as pd

address_json = requests.get(
    "https://raw.githubusercontent.com/element-fi/elf-deploy/main/addresses/mainnet.json"
).json()

res = []
tranche_list = address_json["tranches"]
for tranche_id in tranche_list:
    for tranche in tranche_list[tranche_id]:
        pool = tranche["ptPool"]
        newShit = {key: value for key, value in pool.items()}
        newShit["expiration"] = tranche["expiration"]
        res.append(newShit)
df = pd.DataFrame(res)
df = df.sort_values(by="expiration", ascending=False, ignore_index=True)
df.to_csv("principal_tokens.csv", index=False)
df.to_csv(
    "principal_token_addresses.csv", index=False, columns=["address"], header=False
)
