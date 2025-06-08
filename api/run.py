import uvicorn

import config

if __name__ == "__main__":
    uvicorn.run("api_v1.app:app", 
                host=config.API_HOST, 
                port=config.API_PORT, 
                reload=True) 