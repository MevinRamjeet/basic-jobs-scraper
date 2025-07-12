import requests
from bs4 import BeautifulSoup
import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter


def get_job_details(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    job_details = soup.find_all('div', class_='utf-job-listing-description')

    job_list = []
    for jobs in job_details:
        job_titles = jobs.find_next('h3', class_='utf-job-listing-title')
        job_titles = job_titles.text.title()

        companies = jobs.find_next('i', class_='icon-feather-briefcase').find_next('span')
        companies = companies.text

        salaries = jobs.find_next('i', class_='icon-line-awesome-money').find_next('span')
        salaries = salaries.text

        location = jobs.find_next('i', class_="icon-material-outline-location-on").find_next('span')
        location = location.text

        dates = jobs.find_next('i', class_='icon-material-outline-access-time').find_next('span')
        dates = dates.text.replace('Added: ', '')

        job_list.append([job_titles, companies, location, dates, salaries])
    return job_list


def scrape_jobs():
    admin_jobs_list = []
    accounting_jobs_list = []
    ict_jobs_list = []
    marketing_list = []

    for i in range(1, 3):
        admin_url = f'https://www.jobs.mu/categories/708/administrative-clerical-jobs/?searchId=1723994617.5534&action=search&page={i}'
        accounting_url = f'https://www.jobs.mu/categories/707/accounting-auditing-tax-services-finance-jobs/?searchId=1724162127.7779&action=search&page={i}'
        ict_url = f'https://www.jobs.mu/categories/706/ict-it-web-jobs/?searchId=1724164556.4823&action=search&page={i}'

        admin_jobs_list += get_job_details(admin_url)
        accounting_jobs_list += get_job_details(accounting_url)
        ict_jobs_list += get_job_details(ict_url)

    for i in range(1,4):
        marketing_url = f'https://www.jobs.mu/categories/704/marketing-sales-jobs/?searchId=1724891459.3858&action=search&page={i}'
        marketing_list += get_job_details(marketing_url)

    tourism_url = 'https://www.jobs.mu/jobs/?searchId=1724164621.734&action=search&page=1'
    tourism_jobs_list = get_job_details(tourism_url)

    count_admin = len(admin_jobs_list)
    count_account = len(accounting_jobs_list)
    count_ict = len(ict_jobs_list)
    count_tourism = len(tourism_jobs_list)
    count_market = len(marketing_list)

    print(f'Number of Jobs Found:\n'
          f'Administrative: {count_admin}\n'
          f'Accounting: {count_account}\n'
          f'IT/ICT/WEB: {count_ict}\n'
          f'Tourism: {count_tourism}\n'
          f'Marketing: {count_market}\n'
          f'"""""""""""""""""""""""""')

    while True:
        choice = input('Would you like to save jobs to CSV files? (y or n): ')
        if choice.lower() == 'y':
            save_to_csv(admin_jobs_list, 'admin.csv')
            save_to_csv(accounting_jobs_list, 'accounting.csv')
            save_to_csv(ict_jobs_list, 'ict.csv')
            save_to_csv(tourism_jobs_list, 'tourism.csv')
            save_to_csv(marketing_list, 'marketing.csv')
            print('CSV files have been updated.\n')
            break
        elif choice.lower() == 'n':
            print('CSV files have not been updated.\n')
            break
        else:
            print('Wrong input. Please retry.\n')
            continue


def save_to_csv(joblist, csv_filename):
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(joblist)


def get_list_from_csv(csv_file):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        jobs_list = list(reader)
    return jobs_list


def pie_chart_salary():
    admin_list = get_list_from_csv('admin.csv')
    accounting_list = get_list_from_csv('accounting.csv')
    ict_list = get_list_from_csv('ict.csv')
    tourism_list = get_list_from_csv('tourism.csv')
    marketing_list = get_list_from_csv('marketing.csv')

    salaries = np.concatenate((np.array(admin_list)[:, 4],
                              np.array(accounting_list)[:, 4],
                              np.array(ict_list)[:, 4],
                              np.array(tourism_list)[:, 4],
                              np.array(marketing_list)[:, 4]))

    negotiable = np.count_nonzero(salaries == 'Negotiable')
    undisclosed = np.count_nonzero(salaries == 'Not disclosed')
    above12k = np.count_nonzero(salaries == 'Rs 12,501 - Rs 25,000')
    above25k = np.count_nonzero(salaries == 'Rs 25,001 - Rs 50,000')
    above50k = np.count_nonzero(salaries == 'Rs 50,001 - Rs 75,000')
    above75k = np.count_nonzero(salaries == 'Rs 75,001 - Rs 100,000')

    data = [negotiable, undisclosed, above12k, above25k, above50k, above75k]
    data_labels = ['negotiable',
                   'not disclosed',
                   'Rs 12,501 - Rs 25,000',
                   'Rs 25,001 - Rs 50,00',
                   'Rs 50,001 - Rs 75,000',
                   'Rs 75,001 - Rs 100,000']

    plt.figure(figsize=(10, 8))
    plt.title('Combined Salaries Distribution for Admin, Accounting, IT, Tourism & Marketing')
    plt.pie(data, labels=data_labels, autopct='%.1f%%', wedgeprops={'linewidth': 3.0, 'edgecolor': 'white'})
    plt.show()


def bar_chart_job():
    admin_list = get_list_from_csv('admin.csv')
    accounting_list = get_list_from_csv('accounting.csv')
    ict_list = get_list_from_csv('ict.csv')
    tourism_list = get_list_from_csv('tourism.csv')
    marketing_list = get_list_from_csv('marketing.csv')

    admin_count = len(admin_list)
    acc_count = len(accounting_list)
    ict_count = len(ict_list)
    tourism_count = len(tourism_list)
    market_count = len(marketing_list)

    x_axis = ['Administrative', 'Accounting', 'IT/ICT', 'Tourism', 'Marketing']
    y_axis = [admin_count, acc_count, ict_count, tourism_count, market_count]

    plt.figure(figsize=(10,6))
    plt.title('Number of jobs  by sector')
    plt.barh(x_axis, y_axis)

    for index, value in enumerate(y_axis):
        plt.text(value, index,
                 str(value))

    plt.show()


def bar_chart_date():
    admin_list = get_list_from_csv('admin.csv')
    accounting_list = get_list_from_csv('accounting.csv')
    ict_list = get_list_from_csv('ict.csv')
    tourism_list = get_list_from_csv('tourism.csv')
    marketing_list = get_list_from_csv('marketing.csv')

    dates = np.concatenate((np.array(admin_list)[:, 3],
                            np.array(accounting_list)[:, 3],
                            np.array(ict_list)[:, 3],
                            np.array(tourism_list)[:, 3],
                            np.array(marketing_list)[:, 3]))

    count_dates = Counter(dates)

    date_list = []
    count_list = []
    for date, count in sorted(count_dates.items(), reverse=True):
        date_list.append(date)
        count_list.append(count)

    plt.figure(figsize=(10, 6))
    plt.title('Trend of jobs availability over time')
    plt.plot(date_list, count_list)
    plt.xticks(rotation=45, ha='right')

    plt.show()


def main():
    while True:
        print('"""""""""""""""""""""""""""""""\n'
              '1.  Display Number of jobs by Sector (Bar Chart)\n'
              '2.  Display Salaries Distribution (Pie Chart)\n'
              '3.  Display trend by date (Bar Chart)\n'
              '4.  Scrape Jobs and/or Update CSVs\n'
              '5.  Exit\n'
              '"""""""""""""""""""""""""""""""')
        choice = int(input('Enter Your Choice (1-5): '))

        if choice == 1:
            bar_chart_job()
            continue
        elif choice == 2:
            pie_chart_salary()
            continue
        elif choice == 3:
            bar_chart_date()
            continue
        elif choice == 4:
            print('Searching.....\nPlease wait...')
            scrape_jobs()
            continue
        elif choice == 5:
            print('Exiting...')
            break
        else:
            print('Incorrect input.  Please retry.\n')
            continue


if __name__ == '__main__':
    main()
