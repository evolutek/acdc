from protocol import API, CmdEnum

api = API()
# response = api.write(CmdEnum.SETUP)
# print(f"j'ai recu ceci {response.data}")
# #response = api.write(CMD.BATTERIE)
# print(f"j'ai recu ceci {response.data}")
response = api.write(CmdEnum.PING)
print("bonjour j'ai ping")
# response = api.write(CmdEnum.SET_ANGLE, CmdEnum.AllAngle.CENTER)
