# Import Dependencies

from kafka import KafkaConsumer
from sklearn.externals import joblib
import mysql.connector

# do prediction and save result to mysql database

def predict(data,model):
    
    label = model.predict(data)
    
    #connect to database
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        database="python_DB", 
        user="nazli",
        passwd="N123",
        )
        
    except Exception as e:
        print("Can't connect. Invalid dbname, user or password?")
        print(e)
        
    mycursor =  mydb.cursor(buffered=True)     
    sql = "INSERT INTO attack_detect (Destination_port,label,IP_Addr) VALUES (%s, %s, %S)"
    val = (data[60],label,data[2])
    mycursor.execute(sql, val)

    mydb.commit()     
        



if __name__ == '__main__':
    
    # reload trained Random Forest Model
    Attack_model=joblib.load("s3://attackproof/Attack_model.sav")
    
    #set up kafka consumer
    topics=['cyber']
    consumer = KafkaConsumer(*topics,
                             auto_offset_reset='earliest',
                             bootstrap_servers=['ec2-54-80-57-187.compute-1.amazonaws.com:9092'],
                             api_version=(0, 9),
                             group_id='t9',  # group id is parsed to ensure all the consumner nodes are within the same
                             ),
    
    
    # begin predicting upcoming network data
    for message in consumer:
        elements = message.split(',')
        data=elements[79:140]
        predict(data,Attack_model)
