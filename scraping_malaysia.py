from media_release_scrap__functions import *



# note: the scraped articles are for all entries (ALL YEARS)
def scrap_reg_MY_SC(screen_name, type_of_media, link_html, is_db_accessible, is_display):
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
    regs = BeautifulSoup(html, "html.parser").find('div', class_="com com-f3883a8e-7c9e-4192-8caf-5d1c404699d3 pag-list-01")\
                                            .find_all('div', class_="c1B2M2Y8AsgTpgAmY7PhCfg")
    for reg in regs:
        title_info = reg.find('a', attrs={'data-so-type': 'btn;1'})
        link_2nd_part = str(title_info.get('href'))
        link = "https://www.sc.com.my/" + link_2nd_part
        title = text_format(title_info.find('div', class_="a-inner-text").text)
        # find the first instance of a-inner-text, which happens to be the date
        date_str = (reg.find('div', class_="a-inner-text").text).split(' ')
        date = datetime(int(date_str[2]), month_dict[date_str[1]], int(date_str[0]))
        date_to_id = date.strftime('%y%m%d')
        id = text_format(link, date=date_to_id, is_id=True)
        description = reg.find('div', class_="com com-4f7ed01b-c111-4642-8bf2-a633b289b93a")\
                        .find('div', class_="a-inner-text").text
        description = text_format(description, is_description=True)
        link = text_format(link)
        generate_new_media(screen_name, id, date, title, description, link, type_of_media, old_medias,
                        is_db_accessible, is_display)



# SC | Securities Commission Malaysia
def init_reg_MY_SC(is_db_accessible, is_display):
    screen_name = "SC"
    type_of_media = "Media Release"
    html_link = "https://www.sc.com.my/resources/media/media-release"
    
    try:
        scrap_reg_MY_SC(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-",  type_of_media, "-", "Error:", e)
        
  
  
        
def scrap_reg_MY_BNM(screen_name, type_of_media, link_html, is_db_accessible, is_display):
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
    all_rows = BeautifulSoup(html, "html.parser").find('tbody', id="myTable").find_all('tr')
    for row in all_rows:
        row_entry = row.find_all('td')
        link = row_entry[1].find('a').get('href')
        title = text_format(row_entry[1].find('a').text)
        
        date_str = row_entry[0].find('p').text.strip().split(' ')
        date = datetime(int(date_str[2]), month_dict_short[date_str[1]], int(date_str[0]))
        date_to_id = date.strftime('%y%m%d')
        id = text_format(link, date=date_to_id, is_id=True)
        article_html = requests.get(link).text
        article_content = BeautifulSoup(article_html, "html.parser").find_all('div', class_="article-content-cs")[1]
        first_sentence = (article_content.text.split('. ')[0] + '.').strip()
        generate_new_media(screen_name, id, date, title, first_sentence, link, type_of_media, old_medias,
                            is_db_accessible, is_display)      
        
    
    

# BNM | Bank Negara Malaysia
def init_reg_MY_BNM(is_db_accessible, is_display):
    screen_name = "BNM"
    type_of_media = "Press Release"
    html_link = "https://www.bnm.gov.my/press-release-2022"
    
    try:
        scrap_reg_MY_BNM(screen_name, type_of_media, html_link, is_db_accessible, is_display)
    except Exception as e:
        print(screen_name, "-",  type_of_media, "-", "Error:", e)
        






if __name__ == "__main__":
    
    # init_reg_MY_SC(True, True)
    init_reg_MY_BNM(True, True)
