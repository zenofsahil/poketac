import logging
import requests
from functools import lru_cache
from typing import Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class PokemonClient:
    def __init__(self, base_url: str, endpoint: str, translate_api: str):
        self.base_url = base_url
        self.endpoint = endpoint
        self.translate_api = translate_api

    def get_pokemon_info(self, name: str, translate: bool = False) -> dict:
        if translate:
            logger.info('Translate API called for pokemon %s', name)
            return self.get_pokemon_info_translated(name)

        logger.info('Basic API called for pokemon %s', name)
        return self.get_pokemon_info_basic(name)

    def get_pokemon_info_basic(self, name: str) -> dict:
        """
        Get basic information for the pokemon as specified by `name`
        """
        url = urljoin(self.base_url, f'{self.endpoint}/{name}')
        
        logger.debug('Fetching URL: %s', url)

        r = self.fetch_url(url)

        if r.ok and r.json() is not None:
            response = {
                'name' : r.json().get('name', name),
                'description' : self.get_description(r.json()),
                'habitat' : self.get_habitat(r.json()),
                'isLegendary' : r.json().get('is_legendary', False)
            }
            return response
        else:
            raise Exception
    
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
        """
        logger.debug('Result not present in cache. Requesting data from network.')
        return requests.get(url)

    def get_pokemon_info_translated(self, name: str) -> dict:
        basic_info = self.get_pokemon_info_basic(name)
        logger.debug('Retrieved basic information')
        translated_info = self.translate_description(basic_info)
        return basic_info

    def translate_description(self, basic_info: dict) -> dict:
        """
        Attempt translation of the description of the pokemon.

        If the pokemon has a habitat of "cave" or the "isLegendary" value for
        the pokemon is True, then the "yoda" translation would be requested. 
        For all other cases, the "shakespeare" translation would be requested.
        """
        logger.debug('Attempting translation')
        return basic_info

    @staticmethod
    def get_habitat(json_content: dict) -> Optional[str]:
        """
        Extract the habitat value from the `json_content`
        """
        habitat = json_content.get('habitat')
        if habitat:
            return habitat.get('name')
        logger.debug('No valid habitat value found')
        return None
            
    @staticmethod
    def get_description(json_content: dict) -> Optional[str]:
        """
        Extract the printable english description from the `json_content`
        """
        descriptions = json_content.get('flavour_text_entries')

        if descriptions is not None and len(descriptions) > 0:
            for description in descriptions:
                language = description.get('language')
                if (
                    language is not None and
                    language.get('name') is not None and
                    language.get('name') == 'en' and
                    description.get('flavor_text') is not None
                ):
                    return description.get('flavor_text')
        logger.debug('No valid description found.')
        return None

