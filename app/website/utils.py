import requests
import zipfile
import io
import xml.etree.ElementTree as ET
import logging

from django.utils.translation import get_language
from .models import Item, UserSettings

def selected_language():
    current_language = get_language()

    return current_language

def get_translation(identifier):
        current_language = get_language()
        item = Item.objects.get(identifier=identifier)
        translation = item.translations.filter(language_code=current_language).first()
        translation_base = item.translations.filter(language_code='en').first()
        translation_final=""
        if translation:
            translation_final=translation.name
        elif translation_base:
            translation_final=translation_base.name
        else:
            translation_final=""

        return translation_final

def row_limit(user):
       user_settings = UserSettings.objects.filter(user=user).first()
       row_limit = user_settings.row_limit if user_settings else 1000
       
       return row_limit

class XMLDataProcessor:
    def __init__(self, url, model, field_mappings):
        self.url = url
        self.model = model
        self.field_mappings = field_mappings

    def download_xml(self):
        logging.info(f"Downloading zip file from: {self.url}")
        try:
            response = requests.get(self.url, timeout=60)
            response.raise_for_status()
            logging.info("Download complete")
            return zipfile.ZipFile(io.BytesIO(response.content))
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to download file: {e}")
            return None

    def extract_xml(self, zip_file, xml_file_name=None):
        logging.info("Loading zip file")
        if not xml_file_name:
            xml_file_name = [f for f in zip_file.namelist() if f.endswith('.xml')][0]
        try:
            with zip_file.open(xml_file_name) as xml_file:
                logging.info(f"Found and opened XML file: {xml_file_name}")
                return ET.parse(xml_file).getroot()
        except Exception as e:
            logging.error(f"Error extracting XML file: {e}")
            return None

    def save_data(self, root, parent_element, item_element):
        logging.info("Processing XML elements")
        for item in root.findall(f'.//{parent_element}//{item_element}'):
            data = {}
            for field, xml_tag in self.field_mappings.items():
                data[field] = item.find(xml_tag).text if item.find(xml_tag) is not None else None

            # Log the extracted data
            logging.info(f"Extracted data: {data}")

            if all(data.values()):  # Optional: add validation logic here
                try:
                    self.model.objects.create(**data)
                    logging.info("Saved to database")
                except Exception as e:
                    logging.error(f"Error saving to database: {e}")
            else:
                logging.warning("Missing required fields. Skipping entry.")
        logging.info("Processing completed")


class Global_variables:

    def get_shared_context():
        logout = get_translation('logout')
        add_record = get_translation('add_record')
        submit = get_translation('submit')
        back = get_translation('back')

        return {
            'logout': logout, 
            'add_record': add_record, 
            'submit': submit, 
            'back': back
        }


    