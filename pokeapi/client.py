import logging
import requests
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import Optional
from urllib.parse import urljoin
from requests.models import PreparedRequest
from pokeapi.utils import remove_nonprintable_chars
from pokeapi.exceptions import (
    PokemonAPIHTTPException,
    TranslationAPIHTTPException
)

logger = logging.getLogger(__name__)


class Client(ABC):

    @abstractmethod
    def fetch_url(url: str) -> dict:
        return


class PokemonClient(Client):
    def __init__(self, base_url: str, endpoint: str):
        self.base_url = base_url
        self.endpoint = endpoint

    def get_pokemon_info(self, name: str) -> dict:
        """
        Get basic information for the pokemon as specified by `name`
        """
        url = urljoin(self.base_url, f'{self.endpoint}/{name}')
        
        logger.debug('Fetching URL: %s', url)

        r = self.fetch_url(url)

        response = {
            'name' : r.get('name', name),
            'description' : self.get_description(r),
            'habitat' : self.get_habitat(r),
            'isLegendary' : r.get('is_legendary', False)
        }
        return response
    
    @staticmethod
    @lru_cache
    def fetch_url(url: str) -> dict:
        """
        Fetch information from the given `url`. This method implements a lru_cache
        mechanism so any information requested once will be cached for further 
        requests.

        This could have some downsides as this cache will live within the context of 
        the PokemonClient class definition. This could possibly have potential
        security implications as this will now become a common cache pool for all
        clients requesting data from our API. 

        For production, I would consider separating out caching to its own layer
        using Redis or memcached.

        NOTE: Using the lru_cache on staticmethods does not interfere with garbage
        collection of class instances. However, since the cache will follow the
        lifetime of the class definition, the initialized cache object will 
        continue to exist even after specific instances of the class have been
        garbage collected.

        NOTE: Using in-memory caching would also mean that caches will be specific
        to the worker that the process is being run under. With uvicorn, we usually
        start the app with multiple workers and so this way of caching is not the
        best strategy. A caching layer that could serve all running workers would
        be the ideal solution.
        """
        logger.debug('Result not present in cache. Requesting data from network.')
        r = requests.get(url)

        if r.ok and r.json() is not None:
            return r.json()

        raise PokemonAPIHTTPException(detail=r.reason, status_code=r.status_code)

    @staticmethod
    def get_habitat(json_content: dict) -> Optional[str]:
        """
        Extract the habitat value from the `json_content`
        """
        habitat_dict = json_content.get('habitat')
        if habitat_dict:
            return habitat_dict.get('name')
        logger.debug('No valid habitat value found')
        return None
            
    @staticmethod
    def get_description(json_content: dict) -> Optional[str]:
        """
        Extract the printable english description from the `json_content`
        """
        descriptions = json_content.get('flavor_text_entries')

        if descriptions is not None and len(descriptions) > 0:
            for description in descriptions:
                language = description.get('language')
                if (
                    language is not None and
                    language.get('name') is not None and
                    language.get('name') == 'en' and
                    description.get('flavor_text') is not None
                ):
                    return remove_nonprintable_chars(description.get('flavor_text', ''))
        
        logger.debug('No valid description found.')
        return None

class TranslateClient:
    def __init__(self, translate_url: str):
        self.translate_url = translate_url

    def translate_description(self, basic_info: dict) -> dict:
        """
        Attempt translation of the description of the pokemon.

        If the pokemon has a habitat of "cave" or the "isLegendary" value for
        the pokemon is True, then the "yoda" translation would be requested. 
        For all other cases, the "shakespeare" translation would be requested.

        Can receive code 429 from the translation api.
        """
        logger.info('Attempting translation.')
        translation_kind = self.get_translation_kind(basic_info)
        logger.debug('Attempting "%s" translation.', translation_kind)

        translation_url = urljoin(self.translate_url, f'translate/{translation_kind}')
        request_data = {'text': basic_info.get('description')}

        prepared_request = PreparedRequest()
        prepared_request.prepare_url(translation_url, request_data)

        logger.debug('Attempting translation from url: %s', prepared_request.url)
        translation_req_json = self.fetch_url(prepared_request.url)
        
        translated_description = self.extract_translation(translation_req_json)

        # Return merged dictionary
        return {**basic_info, **{'description': translated_description}}

    @staticmethod
    def extract_translation(response: dict) -> Optional[str]:
        """
        Extract the translation from the the response of the funtranslations API
        """
        translated_description = None
        if (
            response.get('success') is not None and
            response.get('success').get('total', 0) > 0
        ): 
            translated_description = (
                response
                .get('contents')
                .get('translated') 
                if response.get('contents') else None
            )
        return translated_description

    @staticmethod
    def get_translation_kind(basic_info: dict) -> str:
        translation_kind = 'shakespeare'

        habitat = basic_info.get('habitat')
        is_legendary = basic_info.get('isLegendary')
        
        if habitat == 'cave' or is_legendary:
            logger.debug('Habitat detected as %s. Legendary status is %s', habitat, is_legendary)
            translation_kind = 'yoda'

        return translation_kind

    @staticmethod
    @lru_cache
    def fetch_url(url: str) -> dict:
        """
        Please see: `PokemonClient.fetch_url`

        This method is duplicated from PokemonClient and not commonly inherited so that 
        1. The caches for the 2 apis can live separately.
        2. Logic for throwing client specific exceptions will not live together.
        """
        logger.debug('Result not present in cache. Requesting data from network.')
        r = requests.get(url)

        if r.ok and r.json() is not None:
            return r.json()

        raise TranslationAPIHTTPException(detail=r.reason, status_code=r.status_code)
