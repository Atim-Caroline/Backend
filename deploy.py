import os
import logging
from waitress import serve
from social_insights.wsgi import application
from social_insights.settings_prod import DEBUG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/server.log'),
        logging.StreamHandler()
    ]
)

# Get port from environment variable or default to 8000
PORT = int(os.environ.get("PORT", 8000))

# Get host from environment variable or default to 0.0.0.0
HOST = os.environ.get("HOST", "0.0.0.0")

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Print startup message
    logging.info(f"Starting Client Nest server on {HOST}:{PORT}")
    logging.info("Mode: %s", "Debug" if DEBUG else "Production")
    
    # Start Waitress server
    serve(
        application,
        host=HOST,
        port=PORT,
        threads=4,  # Number of worker threads
        url_scheme='https',  # Use HTTPS scheme
        channel_timeout=30,  # Connection timeout in seconds
        cleanup_interval=30,  # How often to clean up inactive connections
    ) 