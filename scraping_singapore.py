from media_release_scrap__functions import *
from selenium import webdriver

def scrap_reg_SG_MAS(screen_name, type_of_media, link_html, is_db_accessible, is_display):
    access_granted = True
    
    try:
        html = requests.get(link_html, proxies=get_proxies(), timeout=10).text
    except Exception as e:
        try:
            sleep(5)
            html = requests.get(link_html, proxies=get_proxies(), timeout=50).text
        except Exception as e:
            access_granted = False
            if is_display:
                print(screen_name, " - Error:", e)
    
    # error check for access to website 
    if not access_granted:
        return

    old_medias = get_old_media(screen_name, is_db_accessible)
    
    html = requests.get(link_html).text
    list_of_regs = BeautifulSoup(html, "html.parser").find('body').find('main', class_='mas-site-main') \
        .find('div', class_="p-x:m").find('div', class_="m-x:a wrap:l").find('div')
        
    

    



def init_reg_SG_MAS(is_db_accessible, is_display):
    screen_name = "MAS"
    type_of_media = "Media Release"
    html_link = "https://www.mas.gov.sg/news?content_type=Media%20Releases&page=1"
    
    try:
       scrap_reg_SG_MAS(screen_name, type_of_media, html_link, is_db_accessible, is_display) 
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)  



if __name__ == '__main__':
    init_reg_SG_MAS(True, True)
    