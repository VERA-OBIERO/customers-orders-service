import africastalking

def send_sms(message, recipients):
    
    username = "sandbox"  
    api_key = "49d74ea7d56d41f7f76a25f408c99a48a2744bd55583cf3dee7721008a9a998d"  

    africastalking.initialize(username, api_key)

   
    try:
        sms = africastalking.SMS
        response = sms.send(message, recipients)
        print(response)  
        return response
    except Exception as e:
        print("Error:", e)
        return None
