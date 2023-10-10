import pandas as pd
import requests

def generateExcelSheet(name, df):
    print(df,"final")
    data = pd.DataFrame(df) 
    filename = f"{name}_Report.xlsx"
    data.to_excel(filename, index=False)   
   

def generate_sheets(tracker_names):
    try:
        dfA = pd.DataFrame({'S.No': [], 'Name': [], 'Rank': [], 'Score': [], 'TimeTaken': []})
        for tracker_name in tracker_names:
            data = []
            for offset in range(0, 1000, 100):
                url = f'https://www.hackerrank.com/rest/contests/{tracker_name}/leaderboard?offset={offset}&limit=100'
                headers = {
                    "User-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36"}
                response = requests.get(url, headers=headers)
                try:
                    response.raise_for_status()
                except:
                    print("Invalid URL or No Internet!")
                    continue
                try:
                    json_data = response.json()
                except:
                    print(f'Error {response.status_code}')
                    continue
                for item in json_data['models']:
                    index = item['index'] + 1
                    name = item['hacker']
                    rank = item['rank']
                    score = item['score']
                    timetaken = item['time_taken']
                    data.append({'S.No': index, 'Name': name, 'Rank': rank, 'Score': score, 'Time Taken': timetaken})

            try:
                df = pd.DataFrame(data)
                dfA = pd.concat([df, dfA], ignore_index=True)
                generateExcelSheet(tracker_name, df)
            except:
                print("Something went wrong.")
                continue
            print(f'Finished: {tracker_name}')

        print("Process Completed: Sheets generated successfully.")
    except:
        print('Something went wrong. This is unexpected. Please try again.')


contest_ids = 'sece-20-24-th-04-10-23'
generate_sheets(contest_ids.split(','))