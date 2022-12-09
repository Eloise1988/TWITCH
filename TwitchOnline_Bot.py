# 1. Start by importing the necessary libraries and setting up the API clients for Telegram and Twitch.
import os
import requests
import json
import threading
from datetime import date

#2. Function that checks whether stream is online
def is_TwitchOnline():
    try:
        # Twitch API parameters
        twitchclient_id="ib0z4bo391ljgud2a8znmimiizc7ea"
        twitchsecret="y7v31nbp22o6c0g############"

        # The Twitch user you are interested in
        userStream='############'


        # URL to request OAuth Token
        tokenurl = 'https://id.twitch.tv/oauth2/token?client_id=' + twitchclient_id + \
                   '&client_secret=' + twitchsecret+'&grant_type=client_credentials'


        response = requests.post(tokenurl)
        response.raise_for_status()
        OAuth_Token = response.json()["access_token"]

        # Connection to Twitch
        response = requests.get('https://api.twitch.tv/helix/streams?user_login=' + \
                   userStream, headers={'Authorization': 'Bearer ' + \
                   OAuth_Token,'Client-Id': twitchclient_id})
        var=json.loads(response.content)


        # Dummy variable stored in text file for status update
        cwd = os.getcwd()
        filename= cwd + '/StreamTwitch_01Bot.txt'
        if (os.path.exists(filename) == False):
            f = open(filename, "w")
            f.write("FALSE")
            f.close()
        else:
            print("File Exists")    

        f = open(filename)
        boolean_online = f.read()
        f.close()

        # Twitch var data returns wether the stream just went live
        if var['data'] and boolean_online.upper()=='FALSE':
            message='Stream of : ['+str(userStream)+'](https://www.twitch.tv/'+str(userStream)+') is online. \n'


            telegram_bot_sendtext(message)
            f = open(filename, "w")
            f.write("TRUE")
            f.close()

        # Twitch var data returns wether the stream just went off-line    
        if not var['data'] and boolean_online.upper()=='TRUE':
            telegram_bot_sendtext(user_login.upper()+' is offline')
            f = open(filename, "w")
            f.write("FALSE")
            f.close()
    
    except Exception as e: 
        print(e)
    
    return "Done"
    
# 3. Function that sends a notification to telegram when stream is on/off-line
def telegram_bot_sendtext(bot_message):
    
    # Fake examples of authorization tokens
    bot_token = '11234485678:AAElJxyzHCbiiZu7Vb_fGGhmk2tbFVr54n'
    bot_chatID = '-1001527664788'
    
    
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
              bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    

    response = requests.get(send_text)

    return response.json()
    
    
# 4 Running a check every 30seconds to see whether the Twitch stream is online
def main():
    timertime=30
    is_TwitchOnline()
   
    # 30sec timer
    threading.Timer(timertime, main).start()
    

# Run the main function
if __name__ == "__main__":
    main()
