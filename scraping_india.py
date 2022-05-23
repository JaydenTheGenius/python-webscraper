from os import access
from media_release_scrap__functions import *
# from selenium import webdriver

# RBI | Reserve Bank of India
def init_reg_IN_RBI(is_db_accessible, is_display):
    screen_name = "RBI"
    
    # Press Release
    try: 
        type_of_media = "Press Release"
        html_link = "https://rbi.org.in/pressreleases_rss.xml"
        scrap_reg_IN_RBI(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)
        


def scrap_reg_IN_RBI(screen_name, type_of_media, link_html, is_db_accessible, is_display):
    access_granted = True

    proxy = urllib.request.ProxyHandler(get_proxies())

    try:
        feed = feedparser.parse(link_html, handlers=[proxy])
    except Exception as e:
        try:
            sleep(5)
            feed = feedparser.parse(link_html, handlers=[proxy])
        except Exception as e:
            access_granted = False
            if is_display:
                print(screen_name, " - Error:", e)
                
    if not access_granted:
        return 
    
    old_medias = get_old_media(screen_name, is_db_accessible)
    print(feed)
    for post in feed.entries:
        title = text_format(post.title)

        date = datetime.fromtimestamp(mktime(post.updated_parsed))
        link = text_format(post.link)
        date_to_id = date.strftime('%y%m%d')
        id = text_format(link, date=date_to_id, is_id=True)
        
# sack coz the page is loaded dynamically 
def scrap_reg_IN_SEBI(screen_name, type_of_media, link_html, is_db_accessible, is_display):
    access_granted = True
    try:
        html = requests.get(link_html, timeout=10).text
    except Exception as e:
        try:
            sleep(5)
            html = requests.get(link_html, timeout=50).text
        except Exception as e:
            access_granted = False
            if is_display:
                print(screen_name, " - Error:", e)
    
    if not access_granted:
        return
    
    old_medias = get_old_media(screen_name, is_db_accessible)
    all_regs = BeautifulSoup(html, "html.parser").find('table').find('tbody').find_all('tr', role="row")
    for reg in all_regs:
        link = reg.find('a').get('href')
        title = reg.find('a').get('title')
        date_str = reg.find('td').text.strip().replace(',', ' ').split()
        date = datetime(int(date_str[2]),int(month_dict_short[date_str[0]]), int(date_str[1]))
        date_to_id = date.strftime('%y%m%d')
        id = text_format(link, date=date_to_id, is_id=True)
        reg_html = requests.get(link).text
        try:
            reg_html = requests.get(link, timeout=10).text
        except Exception as e:
            try:
                sleep(5)
                reg_html = requests.get(link, timeout=50).text
            except Exception as e:
                access_granted = False
                if is_display:
                    print(screen_name, " - Error:", e)
                
        if not access_granted:
            return  
        
        description = BeautifulSoup(reg_html, "html.parser").find('div', class_="textLayer").text
        
        
    
   
   
   
def init_reg_IN_SEBI(is_db_accessible, is_display):
    screen_name = "SEBI"
    
    # Press Release
    type_of_media = "Press Release"
    html_link = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=6&ssid=23&smid=0"
    try:
        scrap_reg_IN_SEBI(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)



    
if __name__ == '__main__':
    init_reg_IN_RBI(True, True)
    init_reg_IN_SEBI(True, True)