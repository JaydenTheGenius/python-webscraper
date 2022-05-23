from os import link
from media_release_scrap__functions import *


# FSC | Financial Services Commission
def init_reg_KR_FSC(is_db_accessible, is_display):
    screen_name = "FSC"
    type_of_media = "Press Release"
    html_link = "https://www.fsc.go.kr/eng/pr010101"
    
    try:
       scrap_reg_AU_FSC(screen_name, type_of_media, html_link, is_db_accessible, is_display) 
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)
        
        
def scrap_reg_AU_FSC(screen_name, type_of_media, link_html, is_db_accessible, is_display):
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
    
    
    html = requests.get(link_html, verify=False).text 
    
    all_articles = BeautifulSoup(html, "html.parser").find('ul', class_="board-list")
    all_regs = all_articles.find_all('li')
    for reg in all_regs:
        link_tag = reg.find('div', class_="cont")
        if not link_tag:
            continue 
        link = "https://www.fsc.go.kr" + link_tag.find('a').get('href')
        
        title = text_format(link_tag.find('a').dt.text.strip())
        
        date_str = str(reg.find('span').text.strip()).replace(',','').split(' ')
        # date in the format year-month-day
        date = datetime(int(date_str[2]),int(month_dict_short[date_str[0]]), int(date_str[1]))
        
        date_to_id = date.strftime('%y%m%d')
        
        id = text_format(title.lower(), date=date_to_id, is_id=True).replace(' ', '')
        
        
        # now to retrieve the description
        full_description = text_format(link_tag.find('a').dd.text.strip())
        first_sentence = text_format(full_description.split('.')[0] + '.', is_description=True)

        generate_new_media(screen_name, id, date, title, first_sentence, link, type_of_media, old_medias,
                       is_db_accessible, is_display)
        


# FSS | Financial Supervisory Service   
def init_reg_KR_FSS(is_db_accessible, is_display):
    screen_name = "FSS"
    type_of_media = "Press Release"
    html_link = "https://english.fss.or.kr/fss/eng/p/news/pr_list.jsp?bbsid=1289277491315#"
    
    try:
       scrap_reg_AU_FSS(screen_name, type_of_media, html_link, is_db_accessible, is_display) 
    except Exception as e:
        print(screen_name, "-", type_of_media, "-", "Error:", e)


def scrap_reg_AU_FSS(screen_name, type_of_media, link_html, is_db_accessible, is_display):
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
    
    html =  requests.get(link_html).text
    reg_entries = BeautifulSoup(html, "html.parser").find('ul', class_="bbsList3 mt20").find_all('li')
    for reg in reg_entries:
        link_2nd_part = reg.find('dd', class_="file").find('a')['href']
        link = "https://english.fss.or.kr/" + link_2nd_part
        title = text_format(reg.find('p', class_="tit").text)
        date_str = (re.sub(' +', ' ', reg.find('span').text.replace(',','').strip())).split(' ')
        date = datetime(int(date_str[2]),int(month_dict[date_str[0]]), int(date_str[1]))
        date_to_id = date.strftime('%y%m%d')
        id = text_format(title.lower().replace('\'', '')\
                        .replace(',', ''), date=date_to_id, is_id=True).replace(' ', '')
        full_desc = reg.find('dd').find('p').text
        first_sentence = text_format((full_desc.split('. ')[0] + '.').strip())
        generate_new_media(screen_name, id, date, title, first_sentence, link, type_of_media, old_medias,
                is_db_accessible, is_display)  


    
    
if __name__ == "__main__":
    init_reg_KR_FSS(True, True)