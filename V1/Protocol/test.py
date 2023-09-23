from protocol import API, CmdEnum

api = API()
response = api.write(CmdEnum.SETUP)
print(f"j'ai recu ceci {response.data}")
# #response = api.write(CMD.BATTERIE)
# print(f"j'ai recu ceci {response.data}")

while True:
    response = api.write(CmdEnum.PING)
    reponse = api.write(CmdEnum.SET_ACC, [0, 50])
    print("bonjour j'ai ping")
# response = api.write(CmdEnum.SET_ANGLE, CmdEnum.AllAngle.CENTER)
