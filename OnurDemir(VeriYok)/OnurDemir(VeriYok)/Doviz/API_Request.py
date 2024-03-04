import requests
import http.client
import json
import os

def requesting():
    url = 'https://v6.exchangerate-api.com/v6/121edced614ee29046def211/latest/TRY'
    
    response = requests.get(url)
    data = response.json()
    
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    months_int = ["01","02","03","04","05","06","07","08","09","10","11","12"]

    with open("Result.json", "w+") as f:
        json.dump(data, f, indent=4)
    
    with open("Result.json", "r") as r:
        result_data = json.load(r)
        date = result_data["time_last_update_utc"][5:16]
        for month in months:
            if month in date:
                index = months.index(month)
                date = date.replace(month, months_int[index])
        date_list = date.split(" ")
        date_list.reverse()
        
        new_date = ""
        for kelime in date_list:
            if date_list.index(kelime) + 1 == len(date_list):
                new_date += kelime
            else:
                new_date += kelime + "-"
                
                
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 593OGshugkupMVDngncaGl:3QxxkfutyBusmxpZ25TiBx"
        }

    conn.request("GET", "/economy/goldPrice", headers=headers)

    res = conn.getresponse()
    data_res = res.read()
    data_res = json.loads(data_res)

    with open("Result.json", "r") as rs:
        rs_veri = json.load(rs)
    for results in data_res["result"]:
        if results["name"] == "Gram Altın":
                rs_veri["conversion_rates"]["GrA"] = 1/float(results["buying"])
        elif results["name"] == "Çeyrek Altın":
                rs_veri["conversion_rates"]["CrA"] = 1/float(results["buying"])
        elif results["name"] == "Yarım Altın":
                rs_veri["conversion_rates"]["YrA"] = 1/float(results["buying"])
        elif results["name"] == "Tam Altın":
                rs_veri["conversion_rates"]["TmA"] = 1/float(results["buying"])
    with open("Result.json", "w") as rsw:
        json.dump(rs_veri, rsw, indent=4)
    
    try:
        os.rename("Result.json", "Result-({}).json".format(new_date))
    except:
        os.remove("Result.json")
        
if __name__ == "__main__":
    requesting()