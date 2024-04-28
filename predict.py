import numpy as np
import places_db_query as place

style=['парк','музей','актив']

def sigmoid(x):
    return 1/(1+np.exp(-x))

def predict(history):
    #print(str(history)+' in predict')
    tuples=[]
    tuples.append(place.selectPlace_data(history[0]))
    tuples.append(place.selectPlace_data(history[1]))
    tuples.append(place.selectPlace_data(history[2]))

    tuples.append([1,'музей',1])
    tuples.append([2,'парк',4])
    #print(tuples[0])

    num_tuples=[]

    for i in range(0,len(tuples),+1):
        if tuples[i][1]==style[0]:
            num_tuples.append([tuples[i][0],0,tuples[0][2]])
        elif tuples[i][1]==style[1]:
            num_tuples.append([tuples[i][0],1,tuples[0][2]])
        else:
            num_tuples.append([tuples[i][0],2,tuples[0][2]])


    result_predict=predict_data(num_tuples)
    result=[result_predict[0],style[result_predict[1]],result_predict[2]]
    return result

def predict_data(num_tuples):
    
    training_inputs=np.array(num_tuples)

    training_outputs=np.array([[1,1,1,0,0]]).T

    np.random.seed()

    synaptic_weights=2*np.random.random((3,1))-1

    #print('random weights:')
    #print(synaptic_weights)

    for i in range (20000):
        input_layer=training_inputs
        outputs=sigmoid(np.dot(input_layer,synaptic_weights))

        err=training_outputs-outputs
        adjustments=np.dot(input_layer.T,err*(outputs*(1-outputs)))

        synaptic_weights+=adjustments

    #print('weights after training')
    #print(synaptic_weights)

    #print('result after training')
    #print(outputs)

    #print(num_tuples[1])

    return num_tuples[1]