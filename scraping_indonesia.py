from media_release_scrap__functions import *

# BI | Bank Indonesia
def init_reg_ID_BI(is_db_accessible, is_display):
    screen_name = "BI"
    
    # News
    type_of_media = "News"
    html_link = "https://www.bi.go.id/en/publikasi/ruang-media/news-release/default.aspx"
    try:
        scrap_reg_ID_BI(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)

        



def scrap_reg_ID_BI(screen_name, type_of_media, link_html, is_db_accessible, is_display):
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
    
    if not access_granted:
        return
    old_medias = get_old_media(screen_name, is_db_accessible)
    html = requests.get(link_html).text
    response = urllib.request.urlopen(link_html)
    print(html)
    all_regs = BeautifulSoup(html, "html.parser").find('div', class_="media-list media-list--no-scroll")\
                            .find_all('div', class_="media media--pers")
    
    for reg in all_regs:
        link = reg.find('a')['href']
        print(link)
        
        
if __name__ == '__main__':
    init_reg_ID_BI(True, True)
    