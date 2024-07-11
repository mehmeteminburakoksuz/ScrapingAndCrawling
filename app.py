import requests
from bs4 import BeautifulSoup




# Ana sayfa URL'si
url = "https://dev.ddos.watch/active-attacks?download=true"

# Ana sayfayı çek ve parse et
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Tablodaki tüm satırları seç
rows = soup.find_all('tr')

# Her satırdaki bilgileri parse et ve sakla
data = []
base_url = "https://dev.ddos.watch"

# İlk satırı başlık olarak kabul etme, veri satırlarını işleme
for row in rows[1:]:
    cells = row.find_all('td')
    if len(cells) > 0:
        # Boş olmayan hücreleri topla
        attack_data = {}
        if len(cells) > 1 and cells[1].get_text(strip=True):
            attack_data['type'] = cells[1].get_text(strip=True)
        if len(cells) > 2 and cells[2].get_text(strip=True):
            attack_data['target'] = cells[2].get_text(strip=True)
        if len(cells) > 3 and cells[3].get_text(strip=True):
            attack_data['events'] = cells[3].get_text(strip=True)
        if len(cells) > 4 and cells[4].get_text(strip=True):
            attack_data['duration'] = cells[4].get_text(strip=True)
        if len(cells) > 5 and cells[5].get_text(strip=True) and cells[5].get_text(strip=True) != "-":
            attack_data['ısp'] = cells[5].get_text(strip=True)

        # "View" linkini bul ve ilgili sayfaya git
        view_link = cells[-1].find('a')
        if view_link and view_link.has_attr('href'):
            view_url = base_url + view_link['href'] + "?download=true"  # download=true ekleniyor
            view_response = requests.get(view_url)
            view_soup = BeautifulSoup(view_response.content, 'html.parser')

            # "View" linkindeki tablodaki bilgileri çek
            table = view_soup.find('table', {'class': 'table'})
            if table:
                rows_in_view = table.find_all('tr')
                for info_row in rows_in_view:
                    info_cells = info_row.find_all('td')
                    if len(info_cells) == 2:
                        key = info_cells[0].get_text(strip=True)
                        value = info_cells[1].get_text(strip=True)
                        attack_data[key] = value

        # Sadece dolu olan verileri ekle
        if attack_data and 'ısp' in attack_data:
            data.append(attack_data)

# Sonuçları yazdır
for item in data:
    print(item)