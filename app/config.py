from pydantic import BaseSettings

#env variables validation to run our application
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_password: str #= "localhost" # : default value giving
    database_username: str #= "postgres"
    secret_key: str #= "121343113535345415"
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
        
settings = Settings()

'''
import os
print(os.environ['HOME']) for system env variable
'''