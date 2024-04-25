import sys
sys.path.insert(0, '..')

import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_KEY')


