from soup import soup_base
from scraper import scraper_base
import time
import csv

startTime = time.time()


scraper = scraper_base(headless=False)

MATCH_ALL = r".*"

def read_ids_in(filename):
    names = []
    titles = []
    npis = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                names.append(row[0])
                titles.append(row[1])
                npis.append(row[2])
                line_count += 1
    return names, titles, npis

def load_page(id_number):
    pageUrl = "https://npidb.org/doctors/allopathic_osteopathic_physicians/vascular-surgery_2086s0129x/"+id_number+".aspx"

    scraper.getPage(pageUrl)

def check_valid():
    soup = soup_base(scraper.browser.page_source)
    isDeactivated = soup.find_by_text_generic('or is invalid', 'h1')
    return isDeactivated

def scrape_specialty_info():
    soup = soup_base(scraper.browser.page_source)
    specialties = soup.find_all_specific('td', 'itemprop', 'medicalSpecialty')

    area = []
    taxonomy = []
    code = []
    provider_type = []
    for specialty in specialties:
        taxonomyElement = soup.find_next(specialty, 'span')
        taxonomySearch = soup.find_next(taxonomyElement, 'span')
        taxonomyText = soup.find_next(taxonomyElement, 'span').text

        specialtyCode = soup.find_next(taxonomySearch, 'td')
        specialtyCodeText = soup.find_next(taxonomySearch, 'td').text

        providerType = soup.find_next(specialtyCode, 'td')
        providerTypeText = soup.find_next(specialtyCode, 'td').text

        area.append(specialty.text)
        taxonomy.append(taxonomyText)
        code.append(specialtyCodeText)
        provider_type.append(providerTypeText)

    return area, taxonomy, code, provider_type

def scrape_profile_info():
    soup = soup_base(scraper.browser.page_source)
    details = soup.find_all_specific('td', 'class', 'bg-warning')
    # print(status)
    for detail in details[1:]:
        if detail.text == 'Status':
            status = soup.find_next(detail, 'td').text
        if detail.text == 'Credentials':
            credentials = soup.find_next(detail, 'td').text
        if detail.text == 'Enumeration date':
            enumeration_date = soup.find_next(detail, 'td').text
        if detail.text == 'Entity':
            entity = soup.find_next(detail, 'td').text
        if detail.text == 'Identifiers':
            identifiers = soup.find_next(detail, 'td').text
        if detail.text == 'Hospital affiliation(s)':
            hospital_affiliations = soup.find_next(detail, 'td').text

    return status, credentials, enumeration_date, entity, identifiers, hospital_affiliations

def scrape_contact_info():
    soup = soup_base(scraper.browser.page_source)
    address = soup.find_all_specific('address', 'class', 'lead')[0].text
    return address

def setup_csv():
    with open('clinician_data.csv', mode='w+') as clinician_file:
        clinician_writer = csv.writer(clinician_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        clinician_writer.writerow(['NAME', 'TITLE', 'NPI', 'ADDRESS', 'SPECIALTY', 'TAXONOMY',
                                   'CODE', 'PROVIDER TYPE', 'STATUS', 'CREDENTIALS',
                                   'ENUMERATION DATE', 'ENTITY', 'IDENTIFIERS', 'HOSPITAL AFFILIATIONS'])

def write_info(name, title, npi, address, specialty, taxonomy, code, provider_type, status, credentials,
               enumeration_date, entity, identifiers, hospital_affiliations):
    with open('clinician_data.csv', mode='a') as clinician_file:
        clinician_writer = csv.writer(clinician_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        clinician_writer.writerow([name, title, npi, address, specialty, taxonomy, code, provider_type, status, credentials,
               enumeration_date, entity, identifiers, hospital_affiliations])
    return


names, titles, npis = read_ids_in('export.csv')
for i in range(0, len(names)):
    if i == 0:
        setup_csv()
    if npis[i] == 'null':
        continue
    load_page(npis[i])
    if check_valid() is not None:
        continue

    specialty, taxonomy, code, provider_type = scrape_specialty_info()
    status, credentials, enumeration_date, entity, identifiers, hospital_affiliations = scrape_profile_info()
    address = scrape_contact_info()
    for j in range(len(specialty)):
        write_info(names[i], titles[i], npis[i], ''.join(s for s in address if ord(s) > 31 and ord(s) < 126), specialty[j], taxonomy[j], code[j], provider_type[j], ''.join(s for s in status if ord(s)>31 and ord(s)<126), ''.join(s for s in credentials if ord(s)>31 and ord(s)<126),
               ''.join(s for s in enumeration_date if ord(s)>31 and ord(s)<126), ''.join(s for s in entity if ord(s)>31 and ord(s)<126), ''.join(s for s in identifiers if ord(s)>31 and ord(s)<126), ''.join(s for s in hospital_affiliations if ord(s)>31 and ord(s)<126))

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))