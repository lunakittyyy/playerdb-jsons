import os
import json
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime

json_folder = 'jsons'

def extract_account_creation_date(account_data):
    if 'AccountCreationDate' in account_data:
        account_creation_date = account_data['AccountCreationDate']

        if 'T' in account_creation_date:
            account_creation_date = account_creation_date.split('T')[0]

        try:
            datetime.strptime(account_creation_date, '%Y-%m-%d')
            return account_creation_date
        except ValueError:
            return None
    return None

dates = []

for filename in os.listdir(json_folder):
    if filename.endswith('.json'):
        filepath = os.path.join(json_folder, filename)
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
                creation_date = extract_account_creation_date(data)
                if creation_date:
                    dates.append(creation_date)
            except json.JSONDecodeError:
                continue

date_counts = Counter(dates)
sorted_dates = sorted(date_counts.items())

dates_sorted = [datetime.strptime(date, '%Y-%m-%d') for date, _ in sorted_dates]
counts_sorted = [count for _, count in sorted_dates]

daily_counts = {}
for date, count in zip(dates_sorted, counts_sorted):
    if date in daily_counts:
        daily_counts[date] += count
    else:
        daily_counts[date] = count


sorted_daily_counts = sorted(daily_counts.items())

dates_for_plotting = [date for date, _ in sorted_daily_counts]
account_creations_for_plotting = [count for _, count in sorted_daily_counts]

plt.figure(figsize=(12, 6))
plt.plot(dates_for_plotting, account_creations_for_plotting, linestyle='-', color='b')

plt.xlabel('Date')
plt.ylabel('Number of Accounts Created')
plt.title('Number of Accounts Created Over Time - ' + str(len(dates)) + ' accounts')

plt.xticks(
    dates_for_plotting[::30],
    [date.strftime('%b %Y') for date in dates_for_plotting[::30]],
    rotation=45
)

plt.tight_layout()


plt.show()
