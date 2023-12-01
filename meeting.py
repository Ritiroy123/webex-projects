import requests
import pandas as pd

def job():
    # Get site URLs from meetingPreferences
    user_email = 'keshav@proactive.co.in'
    site_urls = get_all_site_urls(user_email)

    if site_urls:
        # Initialize an empty DataFrame to store all the data
        all_data = pd.DataFrame()

        for site_url in site_urls:
            # Construct the URL for meetingReports/usage
            url = f'https://webexapis.com/v1/meetingReports/usage?siteUrl={site_url}'
            
            # Make a request to the meetingReports/usage endpoint
            response = requests.get(url, headers={'Authorization': 'Bearer MDQ4YjA3YTgtNjkyZi00Yzg4LTg3YmMtMzdlNmU3MDgyMjMzNjJlOGUyZDUtYjI1_PF84_3bf06e7b-f230-427f-9163-c54d2e428d6a'})
            
            if response.status_code == 200:
                if 'items' in response.json():
                    data = {
                        'meetingId': [],  
                        'meetingNumber': [],
                        'meetingTitle':[],
                        'start':[],
                        'end':[],
                        'duration':[],
                        'scheduledType':[],
                        'hostDisplayName':[],
                        'hostEmail':[],
                        'totalPeopleMinutes':[],
                        'totalCallInMinutes':[],
                        'totalCallOutDomestic':[],
                        'totalCallInTollFreeMinutes':[],
                        'totalCallOutInternational':[],
                        'totalVoipMinutes':[],
                        'totalParticipants':[],
                        'totalParticipantsVoip':[],
                        'totalParticipantsCallIn':[],
                        'totalParticipantsCallOut':[],
                        'peakAttendee':[],
                        'totalInvitee':[],
                        'serviceType':[]
                    }

                    for item in response.json()['items']:
                        # Extract data from the response and append it to the DataFrame
                        data['meetingId'].append(item.get('meetingId'))
                        data['meetingNumber'].append(item.get('meetingNumber'))
                        data['meetingTitle'].append(item.get('meetingTitle'))
                        data['start'].append(item.get('start'))
                        data['end'].append(item.get('end'))
                        data['duration'].append(item.get('duration'))
                        data['scheduledType'].append(item.get('scheduledType'))
                        data['hostDisplayName'].append(item.get('hostDisplayName'))
                        data['hostEmail'].append(item.get('hostEmail'))
                        data['totalPeopleMinutes'].append(item.get('totalPeopleMinutes'))
                        data['totalCallInMinutes'].append(item.get('totalCallInMinutes'))
                        data['totalCallOutDomestic'].append(item.get('totalCallOutDomestic'))
                        data['totalCallInTollFreeMinutes'].append(item.get('totalCallInTollFreeMinutes'))
                        data['totalCallOutInternational'].append(item.get('totalCallOutInternational'))
                        data['totalVoipMinutes'].append(item.get('totalVoipMinutes'))
                        data['totalParticipants'].append(item.get('totalParticipants'))
                        data['totalParticipantsVoip'].append(item.get('totalParticipantsVoip'))
                        data['totalParticipantsCallIn'].append(item.get('totalParticipantsCallIn'))
                        data['totalParticipantsCallOut'].append(item.get('totalParticipantsCallOut'))
                        data['peakAttendee'].append(item.get('peakAttendee'))
                        data['totalInvitee'].append(item.get('totalInvitee'))
                        data['serviceType'].append(item.get('serviceType'))

                    # Append the data for the current site to the overall DataFrame
                    site_data = pd.DataFrame(data)
                    all_data = all_data._append(site_data, ignore_index=True)

                elif response.status_code == 403:
                    pass   
                else:
                    print(f"No meeting data available for site {site_url}.")
            else:
                print(f"Error retrieving data for site {site_url}. Status code: {response.status_code}")

        # Save the combined DataFrame to an Excel file
        excel_filename = 'result_meeting_reports_combined.xlsx'
        all_data.to_excel(excel_filename, index=False)
        print(f"Combined result exported to {excel_filename}")
    else:
        print("Error getting site URLs from meetingPreferences")

def get_all_site_urls(user_email):
    try:
        response = requests.get(
            f'https://webexapis.com/v1/meetingPreferences/sites?userEmail={user_email}',
            headers={'Authorization': 'Bearer Y2E1ODFmOTUtYWUzNi00M2ZlLWJjYjctOGRlYjAzZTBmNzI0YjYzMGM2MzQtOTQ2_PF84_3bf06e7b-f230-427f-9163-c54d2e428d6a'}
        )

        if response.status_code == 200:
            # Check if 'sites' key is present in the response body
            if 'sites' in response.json():
                # Extract site URLs from the response
                site_urls = [site['siteUrl'] for site in response.json()['sites']]
                return site_urls
            else:
                print(f"Error: 'sites' key not found in the response.")
                return None
        else:
            print(f"Error getting site URLs. Status code: {response.status_code}")
            return None
    except Exception as error:
        print(f"Error getting site URLs: {error}")
        return None

# Call the job function
job()
