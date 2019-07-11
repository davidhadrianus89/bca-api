from requests import Session
from bs4 import BeautifulSoup as bs


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
            'mobile':'true'
        }
        authenticate = session.post('https://m.klikbca.com/authentication.do', data=login_data, headers=headers)
        authenticated_page = bs(authenticate.content, 'html.parser')
        try:
            welcome_word = authenticated_page.findAll('font')
        except:
            welcome_word = []

        return session, welcome_word


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
