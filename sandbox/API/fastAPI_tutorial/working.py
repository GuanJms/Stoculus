from fastapi import FastAPI
import uvicorn

from configuration import ConfigurationManager

app = FastAPI()

# GET Request
# POST Sending information
# PUT Updating information
# DELETE Deleting information

config = ConfigurationManager()


@app.get("/get-config/{config_name}")
def get_config(config_name: str):
    match config_name:
        case "path":
            return config.get_path_config()
        case "domain":
            return config.get_domain_config()


@app.post("/create-user")
def create_user(username: str):
    return {"username": username}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=30000)
