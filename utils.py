from requests import Session
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
import time

import pandas as pd

def get_login(username, password):
    with Session() as session:
        site = session.get("https://m.klikbca.com/login.jsp")
        bs_content = bs(site.content, "html.parser")
        user_ip = bs_content.find("input", {"name": "user_ip"})["value"]
        browser_info = bs_content.find("input", {"name": "value(browser_info)"})["value"]
        headers = site.request.headers
        login_data = {
            'value(user_id)':username,
            'value(pswd)':password,
            'value(Submit)':'LOGIN',
            'value(actions)':'login',
            'value(user_ip)':user_ip,
            'user_ip':user_ip,
            'value(mobile)':'true',
            'value(browser_info)':browser_info,
            'mobile':'true',

        }
        authenticate = session.post('https://m.klikbca.com/authentication.do', data=login_data, headers=headers)
        authenticated_page = bs(authenticate.content, 'html.parser')
        try:
            welcome_word = authenticated_page.findAll('font')
        except:
            welcome_word = []

        return session, welcome_word, headers


def get_balance_information(session):
    balance_information = session.post('https://m.klikbca.com/balanceinquiry.do')
    dict_balance = {}
    try:
        soup = bs(balance_information.content, 'html.parser')
        balance_information_table = soup.findAll('font')
        for td in balance_information_table:
            if td.text == 'REKENING':
                dict_balance['No Rekening']=str(balance_information_table[4].text)
            elif td.text == 'SALDO EFEKTIF':
                dict_balance['Sisa Saldo']=str(balance_information_table[6].text)

    except Exception as e:
        # todo: return proper message
        pass
    return dict_balance


def get_mutation_information(session, headers):
    end_date = datetime.now()
    start_date = end_date + timedelta(-30)

    form_data = {
    'value(D1)': 0,
    'value(r1)': 1,
    'value(startDt)': start_date.day,
    'value(startMt)': start_date.month,
    'value(startYr)': start_date.year,
    'value(endDt)': end_date.day,
    'value(endMt)': end_date.month,
    'value(endYr)': end_date.year,
    'value(fDt)':0106,
    'value(tDt)':3006,
    }
    session.get('https://ibank.klikbca.com/nav_bar/account_information_menu.htm', headers=headers)
    statement_history = session.post('https://m.klikbca.com/accountstmt.do?value(actions)=acctstmtview' , headers={'referer':'https://m.klikbca.com/accountstmt.do?value(actions)=acct_stmt'} , params=form_data)
    table_statement = bs(statement_history.content, 'html.parser')

    mutation_summary_dict = {}
    account_info_dict = {}
    try:
        rekening_info = table_statement.findAll('table', {'class':'blue'})[0]
        rows = rekening_info.findAll('tr')
        lines = []
        for tr in rows:
            cols = tr.findAll('td')
            for td in cols:
                text = td.renderContents().strip('\n')
                lines.append(text)
        for line in lines:
            if line == 'NO. REK.':
                account_info_dict['No. Rek'] =lines[3]
            if line == 'NAMA':
                account_info_dict['Nama'] = lines[6]
            if line == 'PERIODE':
                account_info_dict['Periode'] = lines[9]
            if line == 'MATA UANG':
                account_info_dict['Mata Uang'] = lines[12]
    except:
        pass

    try:
        history_table = table_statement.findAll('table', {'class':'blue'})[2]
        rows = history_table.findAll('tr')
        lines = []
        for tr in rows:
            cols = tr.findAll('td')
            for td in cols:
                text = td.renderContents().strip('\n')
                if text == ':':
                    pass
                lines.append(text)
        for line in lines:
            if line == 'SALDO AWAL':
                mutation_summary_dict['Saldo Awal'] =lines[3]
            if line == 'MUTASI KREDIT':
                mutation_summary_dict['Mutasi Kredit'] = lines[6]
            if line == 'MUTASI DEBET':
                mutation_summary_dict['Mutasi Debet'] = lines[9]
            if line == 'SALDO AKHIR':
                mutation_summary_dict['Saldo Akhir'] = lines[12]
        return mutation_summary_dict

    except:
        pass
    return account_info_dict, mutation_summary_dict



session = get_login('davidhad1010', '088919')
print get_mutation_information(session[0], session[2])
session[0].post('https://m.klikbca.com/authentication.do?value(actions)=logout')