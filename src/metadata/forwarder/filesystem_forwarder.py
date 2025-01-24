from pathlib import Path  # Import Path for handling filesystem paths.
from src.metadata.forwarder.forwarder_interface import IForwarder  # Import the IForwarder interface to standardize forwarder behavior.
from src.metadata.utils.constants import SIZE_RECORDS_LIST  # Import constant for batch size calculation.
import json  # Import json for serializing metadata.
import os  # Import os for accessing environment variables.

class FileSystemForwarder(IForwarder):
    """
    A forwarder class that saves metadata to the local filesystem in JSON format.

    Attributes:
        folder_size (int): The number of batches to include in a single folder.
        output_path (Path): The base directory for saving metadata files, derived from the environment variable `METADATA_OUTPUT_PATH`.

    Methods:
        forward(metadata_list: list[dict], batch: int) -> int:
            Saves a list of metadata records to a JSON file in the appropriate folder.
        _get_subfolder(batch: int) -> Path:
            Determines and creates the appropriate subfolder for a given batch.
    """

    folder_size = 1000  # Number of batches per folder.
    output_path = Path(os.environ.get('METADATA_OUTPUT_PATH'))  # Base path for storing metadata files.

    @classmethod
    def forward(cls, metadata_list: list[dict], batch: int) -> int:
        """
        Saves a list of metadata records to a JSON file.

        Args:
            metadata_list (list[dict]): A list of metadata records to save.
            batch (int): The current batch number used for naming files and determining the folder.

        Returns:
            int: 0 if the metadata was successfully written, 1 if an error occurred.
        """
        # Determine the appropriate subfolder for the batch.
        folder = cls._get_subfolder(batch)
        
        # Construct the file name and full file path.
        filename = f"{batch}_{batch + SIZE_RECORDS_LIST}.metadata.json"
        file_path = folder / filename
        
        try:
            # Write the metadata list to a JSON file with proper formatting.
            file_path.write_text(
                json.dumps(metadata_list, ensure_ascii=False, indent=4),
                encoding='utf-8'
            )
            return 0  # Return 0 to indicate success.
        except Exception as e:
            # Log the error if writing fails and return 1.
            print(f"Error writing metadata to {file_path}: {e}")
            return 1

    @classmethod
    def _get_subfolder(cls, batch: int) -> Path:
        """
        Determines and creates the appropriate subfolder for a given batch.

        Args:
            batch (int): The current batch number.

        Returns:
            Path: The Path object representing the subfolder.
        """
        # Calculate the starting batch for the folder based on the folder size.
        batch_start = (batch // cls.folder_size) * cls.folder_size
        
        # Construct the folder name based on the batch range.
        folder_name = f"batch_{batch_start}_{batch_start + cls.folder_size}"
        
        # Create the full folder path.
        path = cls.output_path / folder_name
        
        # Ensure the folder exists, creating it if necessary.
        path.mkdir(parents=True, exist_ok=True)
        return path  # Return the subfolder path.
