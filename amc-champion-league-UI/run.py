import uvicorn
from codebase.utils.config_manager import config
from codebase.utils.logging_config import logger

def main():
    """Run the application with settings from config"""
    app_config = config.get_application_config()
    
    logger.info(f"Starting AMC Champion League API on {app_config['host']}:{app_config['port']}")
    
    uvicorn.run(
        "codebase.app.api:app", 
        host=app_config["host"],
        port=app_config["port"],
        reload=app_config["debug"]
    )

if __name__ == "__main__":
    main()
