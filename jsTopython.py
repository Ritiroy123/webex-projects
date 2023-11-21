import requests
import schedule
import smtplib
import math

def job():
    print('The answer to life, the universe, and everything!')
    status = get_organizations()
    if status == 201:
        print("Data Sync Successfully", "Data Sync Successfull with status code 200")

# def send_mail(subject, text):
#     sender_email = 'ritikaroy85257@gmail.com'
#     receiver_email = 'ritikaroy85257@gmail.com'
#     password = 'Ritikaroy@123'

#     with smtplib.SMTP('smtp.gmail.com', 587) as server:
#         server.starttls()
#         server.login(sender_email, password)
#         message = f'Subject: {subject}\n\n{text}'
#         server.sendmail(sender_email, receiver_email, message)

# def sleep(ms):
#     import time
#     time.sleep(ms / 1000)

def get_zoho_token():
    try:
        data = {
            "accountid": "434653000001059376"
        }
        response = requests.post(
            'https://accounts.zoho.com/oauth/v2/token?refresh_token=1000.3d6ae178a2e29685989160118f75ec99.7d80bb43db46acdef1d34e90c19a7b7d&client_id=1000.XLUX2G854HEVITG926DHT8LHH76G4H&client_secret=f743c69558faf7d852d8e99651b170862268287f51&grant_type=refresh_token',
            headers={'Content-Type': 'application/json'},
            json=data
        )
        access_token = response.json()['access_token']
        print(access_token)
        return access_token
    except Exception as error:
    #     subject = "Geeting Error In Faching data Webex Api"
    #     text = str(error)
    #     mail(subject, text)
        print("get org error")

def get_organizations():
    zoho_new_token = get_zoho_token()

    try:
        response = requests.get(
            'https://webexapis.com/v1/organizations',
            headers={'Authorization': 'Bearer YmQ5ZTVjNGQtZDgxNC00N2E1LTkzZGEtZjBkNWE0YjQyOWUyYzJjM2Q5YTMtYmY5_PF84_3bf06e7b-f230-427f-9163-c54d2e428d6a'}
        )
        count = 0
        used_licence = 0
        issued_licence = 0
        trand_resp = 0

        for item in response.json()['items']:
            last_response = get_licenses(item['id'], item['displayName'], zoho_new_token)
            print("total array data", last_response)

            if last_response is not None and last_response[0] is not None:
                used_licence += last_response[0]['usedlicence']
                issued_licence += last_response[0]['issuedlicence']
                issued_licence += last_response[0]['issuedlicence']
                if last_response[0]['ticketstatus']:
                    count += 1

                print("11newissuedlicence", issued_licence)
                print("11newusedLicence", used_licence)
                print("11ticketstatus", last_response[0]['ticketstatus'])

        for item in response.json()['items']:
            trand_resp += update_trends(item['id'], zoho_new_token)
            print("trandresp", trand_resp)

        print("newissuedlicence", issued_licence)
        print("newusedLicence", used_licence)
        print("trandresp", trand_resp)

        update_org_count(count, issued_licence, used_licence, trand_resp, zoho_new_token)
        return response.status_code

    except Exception as error:
        print("get org error", error)

def update_org_count(org_count, issued_licence, used_licence, trand_resp, zoho_new_token):
    new_json = {
        "Total_License": issued_licence,
        "Used_License": used_licence,
        "Total_Organizations": org_count,
        "Org_Growth_Trend": trand_resp
    }

    new_json2 = [new_json]

    try:
        response2 = requests.post(
            'https://www.zohoapis.com/crm/v2/Webex_Cx_Org_Count',
            headers={
                'Authorization': 'Zoho-oauthtoken ' + zoho_new_token,
                "Content-Type": "application/json"
            },
            json={"data": new_json2}
        )
        print(response2.json())
        print("UpdateOrgCount", response2.status_code)
        return response2.json()

    except Exception as error:
        print("UpdateOrgCount", error)

def change_value_num_to_str(old_val, new_val):
    if old_val is not None:
        total_val = int(old_val) + int(new_val)
    else:
        total_val = int(new_val)
    total = total_val
    print("total", total)
    return total

def append_subsid(old_val, new_val):
    if old_val is not None:
        total_val = old_val + "," + new_val
    else:
        total_val = new_val
    total = total_val
    return total

def get_licenses(org_id, display_name, zoho_new_token):
    try:
        response = requests.get(
            f'https://webexapis.com/v1/licenses?orgId={org_id}',
            headers={
                'Authorization': 'Bearer YmQ5ZTVjNGQtZDgxNC00N2E1LTkzZGEtZjBkNWE0YjQyOWUyYzJjM2Q5YTMtYmY5_PF84_3bf06e7b-f230-427f-9163-c54d2e428d6a'
            }
        )
        new_json = {}
        new_json2 = []
        new_json["Webex_Customer_ID"] = org_id
        new_json["Webex_Customer_Name"] = display_name

        check_subs_id = ""
        total_licence_count = 0
        total_issued_license = 0
        total_used_license = 0

        for item in response.json()['items']:
            if item['name'] == "MS Teams Video":
                if "Integrations_Total_Units" not in new_json:
                    total_licence_count += 1
                new_json["Integrations_Consumed_Units"] = change_value_num_to_str(
                    new_json.get("Integrations_Consumed_Units"), item['consumedUnits'])
                new_json["Integrations_Subscription_Id"] = append_subsid(
                    new_json.get("Integrations_Subscription_Id"), item['subscriptionId'])
                new_json["Integrations_Total_Units"] = change_value_num_to_str(
                    new_json.get("Integrations_Total_Units"), item['totalUnits'])
                check_subs_id = item['subscriptionId']

            if item['name'] == "Meeting 25 party":
                if "Advanced_Space_Meeting_Total_Units" not in new_json:
                    total_licence_count += 1
                new_json["Advanced_Space_Meeting_Consumed_Units"] = change_value_num_to_str(
                    new_json.get("Advanced_Space_Meeting_Consumed_Units"), item['consumedUnits'])
                new_json["advanced_Space_Meeting_Subscription_Id"] = append_subsid(
                    new_json.get("Advanced_Space_Meeting_Subscription_Id"), item['subscriptionId'])
                new_json["Advanced_Space_Meeting_Total_Units"] = change_value_num_to_str(
                    new_json.get("Advanced_Space_Meeting_Total_Units"), item['totalUnits'])
                check_subs_id = item['subscriptionId']

            if item['name'] == "Meeting - Webex Enterprise Edition":
                if "Webex_Meeting_Suit_Total_Units" not in new_json:
                    total_licence_count += 1
                new_json["Webex_Meeting_Suit_Consumed_Units"] = change_value_num_to_str(
                    new_json.get("Webex_Meeting_Suit_Consumed_Units"), item['consumedUnits'])
                new_json["Webex_Meeting_Suit_Subscription_Id"] = append_subsid(
                    new_json.get("Webex_Meeting_Suit_Subscription_Id"), item['subscriptionId'])
                new_json["Webex_Meeting_Suit_Total_Units"] = change_value_num_to_str(
                    new_json.get("Webex_Meeting_Suit_Total_Units"), item['totalUnits'])
                check_subs_id = item['subscriptionId']  

            if item['name'] == "Webex Meetings Assistant":
                if "Webex_Assistant_For_Meeting_Total_Units" not in new_json:
                    total_licence_count += 1
                new_json["Webex_Assistant_For_Meeting_Consumed_Units"] = change_value_num_to_str(
                    new_json.get("Webex_Assistant_For_Meeting_Consumed_Units"), item['consumedUnits'])
                new_json["Webex_Assistant_For_Meeting_Subscription_Id"] = append_subsid(
                    new_json.get("Webex_Assistant_For_Meeting_Subscription_Id"), item['subscriptionId'])
                new_json["Webex_Assistant_For_Meeting_Total_Units"] = change_value_num_to_str(
                    new_json.get("Webex_Assistant_For_Meeting_Total_Units"), item['totalUnits'])
                check_subs_id = item['subscriptionId']   


            if item['name'] == "Webex Event 3,000":
                if "Webex_Webener_3000_Total_Units" not in new_json:
                    total_licence_count += 1
                new_json["Webex_Webener_3000_Consumed_Units"] = change_value_num_to_str(
                    new_json.get("Webex_Webener_3000_Consumed_Units"), item['consumedUnits'])
                new_json["Webex_Webener_3000_Subscription_Id"] = append_subsid(
                    new_json.get("Webex_Webener_3000_Subscription_Id"), item['subscriptionId'])
                new_json["Webex_Webener_3000_Total_Units"] = change_value_num_to_str(
                    new_json.get("Webex_Webener_3000_Total_Units"), item['totalUnits'])
                check_subs_id = item['subscriptionId'] 

            if item['name'] == "Webex Calling - Workspace":
                if "Work_Space_Total_Units" not in new_json:
                    total_licence_count += 1
                new_json["Work_Space_Consumed_Units"] = change_value_num_to_str(
                    new_json.get("Work_Space_Consumed_Units"), item['consumedUnits'])
                new_json["Work_Space_Subscription_Id"] = append_subsid(
                    new_json.get("Work_Space_Subscription_Id"), item['subscriptionId'])
                new_json["Work_Space_Total_Units"] = change_value_num_to_str(
                    new_json.get("Work_Space_Total_Units"), item['totalUnits'])
                check_subs_id = item['subscriptionId']  

            if item['name'] == "Webex Calling - Professional":
                if "Professional_Total_Units" not in new_json:
                    total_licence_count += 1
                new_json["Professional_Consumed_Units"] = change_value_num_to_str(
                    new_json.get("Professional_Consumed_Units"), item['consumedUnits'])
                new_json["Professional_Subscription_Id"] = append_subsid(
                    new_json.get("Professional_Subscription_Id"), item['subscriptionId'])
                new_json["Professional_Total_Units"] = change_value_num_to_str(
                    new_json.get("Professional_Total_Units"), item['totalUnits'])
                check_subs_id = item['subscriptionId']  

            if item['name'] == "Room Systems":
                if "Web_Room_Total_Units" not in new_json:
                    total_licence_count += 1
                new_json["Web_Room_Consumed_Units"] = change_value_num_to_str(
                    new_json.get("Web_Room_Consumed_Units"), item['consumedUnits'])
                new_json["Web_Room_Subscription_Id"] = append_subsid(
                    new_json.get("Web_Room_Subscription_Id"), item['subscriptionId'])
                new_json["Web_Room_Total_Units"] = change_value_num_to_str(
                    new_json.get("Web_Room_Total_Units"), item['totalUnits'])
                check_subs_id = item['subscriptionId']  

            if item['name'] == "Messaging":
                if "Advanced_Messaging_Total_Units" not in new_json:
                    total_licence_count += 1
                new_json["Advanced_Messaging_Consumed_Units"] = change_value_num_to_str(
                    new_json.get("Advanced_Messaging_Consumed_Units"), item['consumedUnits'])
                new_json["Advanced_Messaging_Subscription_Id"] = append_subsid(
                    new_json.get("Advanced_Messaging_Subscription_Id"), item['subscriptionId'])
                new_json["Advanced_Messaging_Total_Units"] = change_value_num_to_str(
                    new_json.get("Advanced_Messaging_Total_Units"), item['totalUnits'])
                check_subs_id = item['subscriptionId']              


            # Add similar blocks for other license types...

        is_issued_licence_zero = 0
        is_used_licence_zero = 0
        issued_lic = 0
        used_lic = 0
        health_score = 0
        keys = new_json.keys()
        total_weightage = 0

        # Health Score Calculations
        for key in keys:
            if key.endswith("_Total_Units"):
                issued_lic += int(new_json[key])
                used_lic += int(new_json[key.replace("Total", "Consumed")])
                weightage = 0.25  # default weightage
                if key.startswith("Advanced_Space_Meeting"):
                    weightage = 0.50
                elif key.startswith("Integrations"):
                    weightage = 0.10
                elif key.startswith("Professional"):
                    weightage = 0.10
                elif key.startswith("Web_Room"):
                    weightage = 0.10
                elif key.startswith("Work_Space"):
                    weightage = 0.10
                elif key.startswith("Webex_Meeting_Suit"):
                    weightage = 0.25
                elif key.startswith("Webex_Webener_3000"):
                    weightage = 0.10
                health_score += (int(new_json[key.replace("Total", "Consumed")]) /
                                 int(new_json[key])) * weightage
                total_weightage += weightage
                is_issued_licence_zero = issued_lic
                is_used_licence_zero = used_lic

        total_health_score = (health_score * 100) / total_weightage

        new_json["Total_Licence_Type"] = total_licence_count
        new_json["Health_Score"] = "{:.2f}".format(total_health_score)

        if 0 <= total_health_score < 25:
            new_json["Health_Score_Analytic"] = "25"
        elif 25 <= total_health_score < 50:
            new_json["Health_Score_Analytic"] = "50"
        elif 50 <= total_health_score < 75:
            new_json["Health_Score_Analytic"] = "75"
        elif 75 <= total_health_score < 100:
            new_json["Health_Score_Analytic"] = "100"
        elif total_health_score >= 100:
            new_json["Health_Score_Analytic"] = "101"

        print("Health_Score_Analytic", new_json["Health_Score_Analytic"])
        print("isusedlicencezero", is_used_licence_zero)
        print("isissuedlicencezero", is_issued_licence_zero)
        print("TotalWeightage", total_weightage)
        print("HealthScore", health_score)
        print(display_name)
        print("totalHealthscore", total_health_score)

        new_json2.append(new_json)

        if check_subs_id and (is_issued_licence_zero != 0 and is_used_licence_zero != 0):
            try:
                response1 = requests.post(
                    'https://www.zohoapis.com/crm/v2/Webex_CX_Licenses_Data',
                    headers={
                        'Authorization': 'Zoho-oauthtoken ' + zoho_new_token,
                        "Content-Type": "application/json"
                    },
                    json={"data": new_json2}
                )
                print("add licenses", response1.status_code)
                return [{
                    'usedlicence': is_used_licence_zero,
                    'issuedlicence': is_issued_licence_zero,
                    'ticketstatus': response1.status_code == 201
                }]
            except Exception as error:
                print("add licenses error", error)
        check_subs_id = ""
        total_licence_count = 0

    except Exception as error:
        print("get licenses error", error, org_id)


def update_trends(org_id, zoho_new_token):
    try:
        response1 = requests.get(
            f'https://www.zohoapis.com/crm/v2/Webex_CX_Licenses_Data/search?sort_order=desc&sort_by=Created_Time&criteria=(Webex_Customer_ID:equals:{org_id})',
            headers={
                'Authorization': 'Zoho-oauthtoken ' + zoho_new_token,
                "Content-Type": "application/json"
            },
        )

        temp_count = 0
        temp_health_score = 0
        current_health_score = 0
        current_id = ""

        if response1.status_code == 200:
            for item in response1.json()['data']:
                if temp_count == 0:
                    current_health_score = item['Health_Score']
                    current_id = item['id']
                if 0 < temp_count < 5:
                    temp_health_score += float(item['Health_Score'])
                temp_count += 1

            trends_data = ((current_health_score - (temp_health_score / (temp_count - 1))) / current_health_score) * 100 if temp_count > 1 else 0.0

            org_growth = 0

            if not isinstance(trends_data, str) and not math.isnan(trends_data):
                if trends_data <= -50:
                    org_growth -= 4
                elif -50 < trends_data < -25:
                    org_growth -= 2
                elif -25 <= trends_data < -10:
                    org_growth -= 1
                elif -10 <= trends_data < 10:
                    org_growth -= 0
                elif 10 <= trends_data < 25:
                    org_growth += 1
                elif 25 <= trends_data < 50:
                    org_growth += 2
                elif trends_data >= 50:
                    org_growth += 4

            print("org_growth", org_growth)

            data1 = {
                "data": [
                    {
                        'id': current_id,
                        'Trends': round(trends_data, 2)
                    }
                ]
            }

            try:
                response2 = requests.put(
                    'https://www.zohoapis.com/crm/v2/Webex_CX_Licenses_Data',
                    headers={
                        'Authorization': 'Zoho-oauthtoken ' + zoho_new_token,
                        "Content-Type": "application/json"
                    },
                    json=data1
                )
                print("add UpdateTrends", response2)
                if not math.isnan(org_growth):
                    return org_growth
                else:
                    return 0
            except Exception as error:
                print("add UpdateTrends error")
            return response2.json()
    except Exception as error:
        print("UpdateTrends error")

job()