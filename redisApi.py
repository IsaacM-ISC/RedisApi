from flask import Flask, request
from flask_restful import Resource, Api
from numpy import require
import redis
import os

app = Flask(__name__)
api = Api(app)

class POP(Resource):
    def post(self):
        r = redis.Redis()#Conexion con Redis
        key = "message_queue"#Nombre de la cola de mensajes
        message = (r.rpop(key)).decode("utf-8") #Sacamos el siguiente valor de la cola
        return {'status': 'Ok','message': message }, 200 #Regresamos el ultimo mensaje de la cola junto con el codigo 200 OK

class PUSH(Resource):
    def post(self):
        r = redis.Redis() #Conexion con Redis
        key = "message_queue" #Nombre de la cola de mensajes
        message = request.args.get('message')#Obtenemos el argumento 'message' de la URL
        r.lpush(key, message)#Insertamos el mensaje a la 'izquierda' de la cola
        return {'status': 'ok'}, 200 #Retornamos el status y el valor 200

class COUNT(Resource):
    def get(self):
        r = redis.Redis()#Conexion con Redis
        key = "message_queue"#Nombre de la cola de mensajes
        count = r.llen(key)#Comando para consultar registros en Redis
        return {'status': 'ok','count': count} ,200 #Devolvemos la cantidad
        

api.add_resource(POP, '/api/queue/pop')
api.add_resource(PUSH, '/api/queue/push')
api.add_resource(COUNT, '/api/queue/count')
if __name__=='__main__':
    app.run()
    #port = int(os.environ.get('PORT', 5000)) #(Para dockerno funcional)
    #app.run(debug=True, host='0.0.0.0', port=port) #(Para docker, no funcional)