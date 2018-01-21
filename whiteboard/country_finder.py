import json
import requests
from whiteboard.models import Message
from urllib.parse import quote
country_list = ['united states', 'russia', 'afghanistan', 'albania', 'algeria', 'american samoa', 'andorra', 'angola', 'anguilla', 'antarctica', 'antigua and barbuda', 'argentina', 'armenia', 'aruba', 'australia', 'austria', 'azerbaijan', 'bahamas', 'bahrain', 'bangladesh', 'barbados', 'belarus', 'belgium', 'belize', 'benin', 'bermuda', 'bhutan', 'bolivia', 'bosnia and herzegowina', 'botswana', 'bouvet island', 'brazil', 'brunei darussalam', 'bulgaria', 'burkina faso', 'burundi', 'cambodia', 'cameroon', 'canada', 'cape verde', 'cayman islands', 'central african rep', 'chad', 'chile', 'china', 'christmas island', 'cocos islands', 'colombia', 'comoros', 'congo', 'cook islands', 'costa rica', 'cote d`ivoire', 'croatia', 'cuba', 'cyprus', 'czech republic', 'denmark', 'djibouti', 'dominica', 'dominican republic', 'east timor', 'ecuador', 'egypt', 'el salvador', 'equatorial guinea', 'eritrea', 'estonia', 'ethiopia', 'falkland islands (malvinas)', 'faroe islands', 'fiji', 'finland', 'france', 'french guiana', 'french polynesia', 'french s. territories', 'gabon', 'gambia', 'georgia', 'germany', 'ghana', 'gibraltar', 'greece', 'greenland', 'grenada', 'guadeloupe', 'guam', 'guatemala', 'guinea', 'guinea-bissau', 'guyana', 'haiti', 'honduras', 'hong kong', 'hungary', 'iceland', 'india', 'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy', 'jamaica', 'japan', 'jordan', 'kazakhstan', 'kenya', 'kiribati', 'korea (north)', 'korea (south)', 'kuwait', 'kyrgyzstan', 'laos', 'latvia', 'lebanon', 'lesotho', 'liberia', 'libya', 'liechtenstein', 'lithuania', 'luxembourg', 'macau', 'macedonia', 'madagascar', 'malawi', 'malaysia', 'maldives', 'mali', 'malta', 'marshall islands', 'martinique', 'mauritania', 'mauritius', 'mayotte', 'mexico', 'micronesia', 'moldova', 'monaco', 'mongolia', 'montserrat', 'morocco', 'mozambique', 'myanmar', 'namibia', 'nauru', 'nepal', 'netherlands', 'netherlands antilles', 'new caledonia', 'new zealand', 'nicaragua', 'niger', 'nigeria', 'niue', 'norfolk island', 'northern mariana islands', 'norway', 'oman', 'pakistan', 'palau', 'panama', 'papua new guinea', 'paraguay', 'peru', 'philippines', 'pitcairn', 'poland', 'portugal', 'puerto rico', 'qatar', 'reunion', 'romania', 'russian federation', 'rwanda', 'saint kitts and nevis', 'saint lucia', 'st vincent/grenadines', 'samoa', 'san marino', 'sao tome', 'saudi arabia', 'senegal', 'seychelles', 'sierra leone', 'singapore', 'slovakia', 'slovenia', 'solomon islands', 'somalia', 'south africa', 'spain', 'sri lanka', 'st. helena', 'st.pierre', 'sudan', 'suriname', 'swaziland', 'sweden', 'switzerland', 'syrian arab republic', 'taiwan', 'tajikistan', 'tanzania', 'thailand', 'togo', 'tokelau', 'tonga', 'trinidad and tobago', 'tunisia', 'turkey', 'turkmenistan', 'tuvalu', 'uganda', 'ukraine', 'united arab emirates', 'united kingdom', 'uruguay', 'uzbekistan', 'vanuatu', 'vatican city state', 'venezuela', 'viet nam', 'virgin islands (british)', 'virgin islands (u.s.)', 'western sahara', 'yemen', 'yugoslavia', 'zaire', 'zambia', 'zimbabwe']

def get_countries_from_text(input_text):
    results = list()
    messages = []
    input_text = input_text.lower()
    for country in country_list:
        if country in input_text:
            results.append(country)
    for entry in results:
        messages.append(get_country_message_from_name(entry))

    return messages

def get_country_message_from_name(country_name):
    base_url ="https://restcountries.eu/rest/v2/name/"
    request = requests.get(base_url + quote(str(country_name)))
    data = request.json()
    flag_url = ""
    wiki_url = ""
    info_string = "Currency: [1], Languages:[3], Capital:[1]"
    currency_string = ""
    language_string = ""
    capital_string = ""
    country_name = country_name
    for entry in data:
        if not "capital" in entry or ("capital" in entry and entry["capital"] == ""):
            continue
        if "flag" in entry and "name" in entry:
            flag_url = entry["flag"]
            wiki_url = "https://en.wikipedia.org/wiki/" + quote(str(entry["name"]))
            if "currencies" in entry and len(entry["currencies"]) > 0:
                currency_string = "Currencies: "
                for currency in entry["currencies"]:
                    if "name" in currency:
                        currency_string += str(currency["name"]) + " "
            if "languages" in entry and len(entry["languages"]) > 0:
                language_string = "Languages: "
                for language in entry["languages"]:
                    if "name" in language:
                        language_string += str(language["name"]) + " "
            if "capital" in entry:
                capital_string = "Capital: " + str(entry["capital"])
    country_description = currency_string + language_string + capital_string
    country_message = Message(message_title=country_name.title(), message_text=country_description, img_url=flag_url,
                              message_link=wiki_url)
    return country_message



if __name__ == "__main__":
    sample_text = "The United States is a country, ice cream is not, Russia is."
    results = get_countries_from_text(sample_text)
    for country in results:
        message = get_country_message_from_name(country)
