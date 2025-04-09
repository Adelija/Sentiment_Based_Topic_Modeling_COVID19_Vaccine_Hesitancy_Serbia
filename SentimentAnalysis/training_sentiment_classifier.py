import pandas as pd
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, ElectraForSequenceClassification, Trainer, TrainingArguments
from dataset import TweetsDataset
import pickle

# LOAD THE ANNOTATED DATA
tweets=pd.read_pickle('sentiments_annotated.pickle')

# SPLIT THE DATA
train, valid = train_test_split(tweets, test_size=.2)
train.reset_index(drop=True,inplace=True)
valid.reset_index(drop=True,inplace=True)

valid, test = train_test_split(valid, test_size=.5)
test.reset_index(drop=True,inplace=True)
valid.reset_index(drop=True,inplace=True)

# LOAD THE MODEL AND TOKENIZER
modelname='classla/bcms-bertic'  
tokenizer = AutoTokenizer.from_pretrained(modelname)
model = ElectraForSequenceClassification.from_pretrained(modelname, num_labels=3)

# PREPARE DATASETS
train_encodings = tokenizer(train['text'].to_list(), is_split_into_words=False, padding=True, truncation=True)
val_encodings = tokenizer(valid['text'].to_list(), is_split_into_words=False, padding=True, truncation=True)
test_encodings = tokenizer(test['text'].to_list(), is_split_into_words=False, padding=True, truncation=True)

train_labels=train['label'].to_list()
val_labels=valid['label'].to_list()
test_labels=test['label'].to_list()

train_dataset = TweetsDataset(train_encodings, train_labels)
val_dataset = TweetsDataset(val_encodings, val_labels)
test_dataset = TweetsDataset(test_encodings, test_labels)

filename = './train_sentiments.pickle'
outfile = open(filename,'wb')
bb=[train_dataset, train['id']]
pickle.dump(bb,outfile)
outfile.close()

filename = './val_sentiments.pickle'
outfile = open(filename,'wb')
bb=[val_dataset, valid['id']]
pickle.dump(bb,outfile)
outfile.close()

filename = './test_sentiments.pickle'
outfile = open(filename,'wb')
bb=[test_dataset, test['id']]
pickle.dump(bb,outfile)
outfile.close()

# TRAINING ARGUMENTS
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=6,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=64,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    save_steps=200,
    evaluation_strategy='steps',
    eval_steps = 200,
    save_total_limit = 10,
    load_best_model_at_end=True
    )

# TRAIN
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset
    )

trainer.train()

# SAVE
model_path = "./BERTICsentiments"  
model.save_pretrained(model_path)
tokenizer.save_pretrained(model_path)
