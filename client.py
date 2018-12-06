from socket import *
import time
buffsize = 2048

def main():
    client_scoket = socket(AF_INET,SOCK_STREAM)
    client_scoket.connect(('127.0.0.1',8889))
    print("welcome to chatroom")
    while True:
        text = input('what do you want to do : ')
        client_scoket.send(text.encode())
        if text == "q":     # 退出聊天室
            print('welcome to back')
            break
        elif text == "g":   # 得到消息
            time.sleep(0.5)
            context = client_scoket.recv(buffsize)
            context = context.decode()
            try:
                
                context = context.split('$')
                for i in context:
                    print(i)
            except:
                print(context)
            
        elif text == "s":   # 发送消息
            text = input('($ in end)\nsiliao --> [name]:[message]\n: ')
            client_scoket.send(text.encode())

        else:               # 如果都不满足提醒该怎么发消息
            try:            
                x = str(text).split(' ')
                if 'login' in x[0] or 'register' in x[0]:
                    # print(x)
                    context = client_scoket.recv(buffsize)
                    print(context.decode())
                else:
                    print('s --> send message\ng --> get message\nq --> quit\nregister [username] [password]\nlogin [username] [password]')
            except:
                print('s --> send message\ng --> get message\nq --> quit\nregister [username] [password]\nlogin [username] [password]')

if __name__ == '__main__':
    main()
