from abc import ABC  # Import the ABC (Abstract Base Class) module to define abstract base classes.

class ITransformer(ABC):
    """
    An abstract base class (ABC) that serves as an interface for all transformer classes.

    Transformer classes inheriting from `ITransformer` should implement specific 
    transformation logic to process and modify log data.

    This class does not define any methods but acts as a marker interface to enforce 
    consistency across all transformers.
    """
    pass  # Placeholder indicating no additional implementation is provided in the base class.
