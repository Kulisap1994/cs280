import os
from Utils import utils
import pickle
import random

label_fileName = 'labels'
data_folderName = 'data'



spam_set = []
ham_set = []

labels_dir = os.path.dirname(os.path.abspath(label_fileName))
data_dir = os.path.join(labels_dir, data_folderName)


with open(label_fileName) as labels:
	for l in labels:
		# label: spam or ham
		# document_path: get the RELATIVE path of each document data/XXX/YYY
		label, document_path = l.strip().split(' ')	
		
		# This part will get the FULL PATH of each document .../data/XXX/YYY.
		document_path = os.path.join(data_dir, document_path)
		

			
		with open(document_path, encoding='latin-1') as raw_file:
					cleaned_data = utils(label, raw_file)
					#print(cleaned_data.tokenized())

					folder_index = int(document_path.split('/')[2])
					print('folder index:', document_path)
					
					if label == 'spam':
						spam_set.append((cleaned_data.tokenized(),label))
					else:
						ham_set.append((cleaned_data.tokenized(),label))
'''
print('pickle mode')

with open('train.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(training_set, filehandle)

with open('test.data', 'wb') as filehandle:
    # store the data as binary data stream
    pickle.dump(test_set, filehandle)
	
print('done')'''
print('spam: ', len(spam_set))
print('ham: ', len(ham_set))
#random.shuffle(data)
train_spam = spam_set[: int((len(spam_set)+1) *.80)]
train_ham = ham_set[: int((len(ham_set)+1) *.80)]

print('train_spam: ', len(train_spam))
print('train_ham: ', len(train_ham))

test_spam = spam_set[int((len(spam_set)+1) *.80): ]
test_ham = ham_set[int((len(ham_set)+1) *.80): ]

print('test_spam: ', len(test_spam))
print('test_ham: ', len(test_ham))

print('pickle mode')

os.remove('train.data')
with open('train.data', 'wb') as filehandle:
	training_set = train_spam + train_ham
	print('training data: ', len(training_set))
	pickle.dump(training_set, filehandle)

os.remove('test.data')
with open('test.data', 'wb') as filehandle:
	test_set = test_spam + test_ham
	print('test data: ', len(test_set))
	pickle.dump(test_set, filehandle)