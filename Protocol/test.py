from protocol import API, CMD

api = API()
response = api.write(CMD.SETUP)
print(f"j'ai recu ceci {response.data}")