import chardet
import os
filename="./Qdata/index.txt"
vocab={}
documents=[] #an array of array of words in each problem heading 


with open(filename) as f:
    lines=f.readlines()

def preprocess(doc_text):
    terms = [term.lower() for term in doc_text.strip().split(" ")[1:]]
    # print(terms)
    return terms

for index, line in enumerate(lines):
    data = []
    data_tokens=[]
    with open(f"./Qdata/data/{index+1}/{index+1}.txt", 'r', encoding="utf-8") as f:
        for l in f:
            if ("Example") in l:
                break
            terms = [term.lower() for term in l.strip().split(" ")]
            for term in terms:
                data_tokens.append(term)
            data.append(terms)
    if not os.path.exists("./tf-idf/Documents/"+f"{index+1}"):
        os.mkdir("./tf-idf/Documents/"+f"{index+1}")
        
    with open("./tf-idf/Documents/"+f"{index+1}/{index+1}.txt", 'w', encoding="utf-8") as f:
        for l in data:
            f.write(" ".join(l)+"\n")
    data_tokens=list(set(data_tokens))
    for token in data_tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1
    tokens = preprocess(line)
    documents.append(tokens)
    tokens = list(set(tokens))
    for token in tokens:
        if token not in vocab:
            vocab[token] = 1
        else:
            vocab[token] += 1

vocab=dict(sorted(vocab.items(),key=lambda item:item[1],reverse=True))
#save the vocab in a text file
with open('./tf-idf/vocab.txt','w',encoding="utf-8") as f:
    for key in vocab.keys():
        f.write(key+"\n")

with open('./tf-idf/idf-values.txt','w') as f:
    for key in vocab.keys():
        f.write(str(vocab[key]))
        f.write("\n")

with open("./tf-idf/documents.txt", 'w') as f:
    for document in documents:
        f.write(" ".join(document)+"\n")

#We create an inverted index which keeps track for each word the document/heading it is present in along with it's term frequency 
inverted_index1 = {}
inverted_index2 = {}
documents_text=[]


for index, document in enumerate(documents):
    with open(f"./tf-idf/Documents/{index+1}/{index+1}.txt",'r',encoding="utf-8") as f:
        data_array=[]
        for l in f:
            data_values=[term.lower() for term in l.strip().split(" ")]
            for v in data_values:
                data_array.append(v)
        documents_text.append(data_array)
    for token in document:
        if token not in inverted_index1:
            inverted_index1[token] = [index]
        else:
            inverted_index1[token].append(index)


for index,document in enumerate(documents_text):
    for token in document:
        if token not in inverted_index2:
            inverted_index2[token] = [index]
        else:
            inverted_index2[token].append(index)



with open("./tf-idf/inverted-index.txt", 'w',encoding="utf-8") as f:
    for key in inverted_index1:
        f.write(f"{key}\n")
        f.write(" ".join(str(doc_id) for doc_id in inverted_index1[key])+"\n")
        if key not in inverted_index2:
            f.write("\n")
        else:
            f.write(" ".join(str(doc_id) for doc_id in inverted_index2[key])+"\n")
    for key in inverted_index2:
        if key not in inverted_index1:
            f.write(f"{key}\n")
            f.write("\n")           
            f.write(" ".join(str(doc_id) for doc_id in inverted_index2[key])+"\n")
 