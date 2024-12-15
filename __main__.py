import os
from dotenv import load_dotenv
from app import create_app, AppEnvironment
load_dotenv()
print(f"API_KEY from .env: {os.getenv('API_KEY')}")
print(f"API_KEY from .env: {os.getenv('FLASK_APP')}")
def require_env(name: str) -> str:
    value =os.getenv(name)
    if value is None:
        raise Exception(f"Failed to read {name} from the environment")
    return value


port = os.environ.get('PORT', 5001)

app_environment = AppEnvironment(
    #csv_location=os.environ.get('CSV_LOCATION', 'https://projects.fivethirtyeight.com/soccer-api/club/spi_matches.csv'),
    #season=2023,
    api_key=require_env('API_KEY'),
    flask_app=require_env('FLASK_APP'),
    flasK_env=require_env('FLASK_ENV'),
)

create_app(app_environment).run(debug=True, host="0.0.0.0", port=int(port))
