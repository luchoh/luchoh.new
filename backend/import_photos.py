
import os
from dotenv import load_dotenv
from app.utils.import_images import main

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    # Run the import utility
    main()