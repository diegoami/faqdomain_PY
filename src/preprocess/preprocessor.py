
from .lists import *
from textacy.preprocess import preprocess_text
import regex

from common import map_products, replace_strings

IBAN_REGEX = regex.compile('DE\d{2}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{4}[ ]\d{2}|DE\d{20}')
TELEPHONE_REGEX = regex.compile('[0-9\-\(\)\+\s]{8,24}')
class Preprocessor:
    def __call__(self, text):
        return self.custom_preprocess(text)

    def replace_bank_names(self, text):
        text = map_products(text, products_map)
        text = replace_strings(text, first_banks, first_bank_name)
        text = replace_strings(text, second_banks, second_bank_name)
        text = replace_strings(text, companies, company_name)

        text = IBAN_REGEX.sub('IBAN', text)

        text = TELEPHONE_REGEX.sub(' TELEPHONE ', text)

        return text

    def replace_characters_to_space(self, text):
        for index, ctos in enumerate(characters_to_space):
            text = text.replace(ctos , characters_spaced[index])
        return text


    def custom_preprocess(self, text):
        text = self.replace_bank_names(text)
        text = preprocess_text(text, fix_unicode = True, lowercase = False, no_urls = True, no_emails = True, no_phone_numbers = True, no_punct = False, no_numbers=False)
        text = self.replace_characters_to_space(text)
        return text
