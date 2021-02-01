from bs4 import BeautifulSoup
import pandas as pd
import requests

def main():
    dn_response = requests.get("https://www.dn.se/")
    dn_html = BeautifulSoup(dn_response.text, "html.parser")

    teaser_container = dn_html.find_all('div', {'class': 'teaser-package__content'})

    master_list = []

    for teaser in teaser_container:
        data_dict = {}
        tc = teaser.find("div", {"class": "teaser__content"})

        try:
            title = ' '.join(tc.h1.text.split())
            title = title.replace('•', '').strip()
            data_dict['Title'] = title
        except:
            continue
        
        try:
            subtitle = ' '.join(tc.p.text.split())
            subtitle = subtitle.replace('•', '-').replace('TV | TEXT', '').replace('LIVE', '').strip()
            data_dict['Subtitle'] = subtitle
        except:
            data_dict['Subtitle'] = ''
        
        try:
            link = 'https://www.dn.se'+teaser.find('a')['href']
            data_dict['Link'] = link
        except:
            pass
        master_list.append(data_dict)

    df = pd.DataFrame(master_list)

    from datetime import datetime
    date = datetime.today().strftime('%Y-%m-%d_%H:%M:%S')
    output_dir = 'output'
    try:
        df.to_csv(f'{output_dir}/DN_Förstasidan_{date}.csv', index=False)
        print('.csv file exported successfully!')
    except:
        print('Error exporting file!')

if __name__ == "__main__":
    main()
