import numpy as np
import places_db_query as place

style=['парк','музей','актив','ресторан']

def __sigmoid(x):
    return 1/(1+np.exp(-x))

def predict(history):#main def
    """функция предсказания следующего места по истории пользователя"""
    #history - массив истории пользователя из БД
    #print(history)
    tuples=__tuple_item1_StrToInt(history) #преобразование каждой [2, 'парк', 3] в [2, 1, 3]
    #print(tuples)
    divider = max([item for sublist in tuples for item in sublist])
    #tuples = [[float(x)//divider for x in tuple1] for tuple1 in tuples]
    for i in range(0, len(tuples)):
        for j in range(0, len(tuples[i])):
            tuples[i][j] = (float(tuples[i][j])/divider)
    #print(f'приведенная история пользователя: {tuples}')

    tuples_input=np.transpose([tuples[0],tuples[1],tuples[2]]) #транспонирование матрицы для обучения
    tuples_output=tuples[3] #результаты для обучающей матрицы
    main_tuples=np.transpose([tuples[1],tuples[2],tuples[3]]) #транспонирование матрицы для результата
    result_predict=__predict_data(tuples_input,tuples_output,main_tuples) #результат нейронной сети
    #print(result_predict)

    #for i in range(0, len(result_predict)):
    #    result_predict[i] = int(result_predict[i]*divider)
    result_predict = [int(x*divider) for x in result_predict]
    #print(f'приведенный результат: {result_predict}')

    result=[int(result_predict[0]),style[int(result_predict[1])],int(result_predict[2])]
    return result

def __predict_data(num_tuples_in,num_tuples_out,main_tuples):
    """создание нейронной сети, ее обучение и вывод результата"""
    
    #print('-----------------')
    training_inputs=np.array(num_tuples_in)
    #print(training_inputs)

    training_outputs=np.array([num_tuples_out]).T
    #print(training_outputs)

    np.random.seed()

    synaptic_weights=2*np.random.random((3,1))-1

    #print('random weights:')
    #print(synaptic_weights)

    for i in range (10000):
        input_layer=training_inputs
        outputs=__sigmoid(np.dot(input_layer,synaptic_weights))

        err=training_outputs-outputs
        adjustments=np.dot(input_layer.T,err*(outputs*(1-outputs)))

        synaptic_weights+=adjustments

    #print('weights after training')
    #print(synaptic_weights)

    #print('result after training')
    #print(outputs)

    #print(num_tuples[1])
    main_output=[]
    for i in range (0,len(main_tuples),+1):
        new_num_tuple=(np.array(main_tuples))[i]#нужно отправить соответствующие последовательности!!!!!!!!!!!!!!!!!
        #print(new_num_tuple)
        output=__sigmoid(np.dot(new_num_tuple,synaptic_weights))
        #print(output)
        #main_output.append(int(round(output[0])))
        main_output.append(output[0])
    #print('main result: '+str(main_output))
    return main_output

def __tuple_item1_StrToInt(history):
    """преобразование второй характеристики каждого элемента массива из строки в число"""
    tuples=[]
    for i in range(0,len(history),+1):
        place_info=place.selectPlace_data(history[i])#place_info - информация о месте в виде [2, 'парк', 3]

        new_item=[place_info[0],1,place_info[2]]
        new_item[1]=1+[i for i,x in enumerate(style) if place_info[1] in x][0]#преобразование 'парк' в 1, 'музей' в 2 и т д
        #new_item - информация о месте в виде [2, 1, 3]
        tuples.append(new_item)
    return tuples
