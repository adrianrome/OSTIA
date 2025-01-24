from src.metadata.parser.parser_interface import IParser  # Import the IParser interface for standardizing parsers.
from typing import Dict, List, Any  # Import type annotations for better clarity and code tooling support.

class DimParser(IParser):
    """
    A parser class for transforming metadata into a structured format.

    This parser processes metadata dictionaries into a standardized format with 
    metadata keys constructed from schema, element, qualifier, and language fields.

    Methods:
        parse(metadata: dict) -> list[dict]:
            Parses the input metadata into a structured list of dictionaries.
    """

    @classmethod
    def parse(cls, metadata: dict) -> list[dict]:
        """
        Parses metadata into a standardized format.

        This method processes each metadata entry by constructing a metadata key
        using the fields `@mdschema`, `@element`, `@qualifier`, and `@lang`. The
        values are extracted and decoded to handle special characters.

        Args:
            metadata (dict): A dictionary containing metadata to parse. Each entry 
                in the dictionary should include fields such as `@mdschema`, `@element`,
                `@qualifier`, `@lang`, and `#text`.

        Returns:
            list[dict]: A list containing a single dictionary of parsed metadata, where
                keys are constructed from metadata attributes, and values are decoded strings.
        """
        upcommons_metadata = {}  # Initialize a dictionary to hold the parsed metadata.

        # Iterate through each metadata entry for parsing.
        for data in metadata:
            # Extract metadata fields for constructing the key.
            schema = data.get('@mdschema')
            element = data.get('@element')
            qualifier = data.get('@qualifier')
            lang = data.get('@lang')
            
            # Construct the metadata key by combining schema, element, qualifier, and lang.
            metadata_key = '.'.join(filter(None, [schema, element, qualifier, lang]))

            # Decode the metadata value, handling special characters and errors.
            metadata_value = data.get('#text', '').encode('latin-1', errors='ignore').decode('unicode-escape', errors='ignore')

            # Check if the key already exists in the dictionary.
            if metadata_key in upcommons_metadata:
                # If the value is already a list, append the new value.
                if isinstance(upcommons_metadata[metadata_key], list):
                    upcommons_metadata[metadata_key].append(metadata_value)
                else:
                    # Convert the existing value into a list and add the new value.
                    upcommons_metadata[metadata_key] = [upcommons_metadata[metadata_key], metadata_value]
            else:
                # Add the new key-value pair to the dictionary.
                upcommons_metadata[metadata_key] = metadata_value

        # Return the parsed metadata as a list containing a single dictionary.
        return [upcommons_metadata]
