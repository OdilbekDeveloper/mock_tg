import requests

class Payme:
    def __init__(self, mycard):
        self.mycard = mycard

    def create(self, summ, desc="#d3smon"):
        summa = summ * 100
        result = dict()

        response = requests.post('https://payme.uz/api/p2p.create',
        json={"method":"p2p.create","params":{"card_id": self.mycard,"amount": summa,"description": desc}},
        headers={'device': '6Fk1rB', 'user-agent': 'Mozilla/57.36'},).json()

        if "result" in response:
            result['ok'] = True
            result['result'] = {}
            result['result']['id'] = response['result']['cheque']['_id']
            result['result']['amount'] = f'{summ} UZS'
            result['result']['pay_url'] = 'https://checkout.paycom.uz/{}'.format(response['result']['cheque']['_id'])
        else:
            result['ok'] = False
            result['error'] = response['error']

        return result


    def info(self, check_id):
        result = dict()
        
        response = requests.post('https://payme.uz/api/cheque.get',
        json={"method":"cheque.get","params":{"id": check_id}},
        headers={'device': '6Fk1rB', 'user-agent': 'Mozilla/57.36'},).json()
        
        try:
            r = response['result']['cheque']['pay_time']
            if(r):
                result['ok'] = True
                result['payment'] = 'successfully'
            else:
                result['ok'] = True
                result['payment'] = 'unsuccessfully'
        except:
            result['ok'] = False
            result['error'] = response['error']
            
        return result
        

s = Payme('63ae5a56f9b3d2b5a8f47cd2') #Payme Card id raqami
print(s.create(1000)) #To'ov summasi
# print(s.info("63de9c255b316b584bf8951a")) #Check id raqamini kiriting