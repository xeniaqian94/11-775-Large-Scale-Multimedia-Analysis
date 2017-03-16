import random


# print "is data 1236? "+str(len(data)==1236)
for name in ['P001','P002','P003']:
   for round in range(3):

      with open("train_dev", "r") as f:
         data = f.read().split('\n')
      # print data[:5]
      # print "is data length 1237? "+str(len(data)==1237)

      data=[line for line in data if len(line)>0]
      print "is data length 1236? "+str(len(data)==1236)

      data=[line if line.split(" ")[1]==name else line.split(" ")[0]+" NULL" for line in data]

      random.shuffle(data)

      training_data = data[:824]
      validation_data = data[824:]
      print "is validation data 412? "+str(len(validation_data)==1236)

      f_train=open(name+"_train_"+str(round),"w")
      f_train.write("\n".join(training_data))
      f_train.close()

      f_validation=open(name+"_validation_"+str(round),"w")
      f_validation.write("\n".join(validation_data))
      f_validation.close()

      f_validation_label=open(name+"_validation_label_"+str(round),"w")
      f_validation_label.write("\n".join(["1" if not line.split()[1]== "NULL" else "0" for line in validation_data]))
      f_validation_label.close()

