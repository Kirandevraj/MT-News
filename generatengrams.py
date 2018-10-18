limit = 1

def ngrams(lines):
    global limit
    ngrams = []
    for i in range(1, limit+1):
        ndict = {}
        for line in lines:
            nline = ['<START>']*i + line + ['<END>']*i
            for x in range(len(nline)- i) :
                key = '_'.join(nline[x:x+i])
                if key in ndict.keys():
                    ndict[key] += 1
                else:
                    ndict[key] = 1
        ngrams += [ndict]
    return ngrams

def cleanLines(lines):
    
    for i in range(len(lines)):
        lines[i] = lines[i][:-1].split()
        for x in range(len(lines[i])):
            lines[i][x] = lines[i][x].lower()
    return lines

def score(uinput, data):
    global limit
    scores = []
    uinput = [uinput.lower().split()]
    cur_ngramsdict = ngrams(uinput)
    for key in data:
        para = cleanLines(data[key].split())
        ngramsdict = ngrams(para)
        fscore = 0.0
        for i in range(len(cur_ngramsdict)):
            cur_dict = cur_ngramsdict[i]
            ansdict = ngramsdict[i]

            precision = 0
            for i in cur_dict.keys():
                if i in ansdict.keys():
                    precision+=1

            recall = 0
            for i in ansdict.keys():
                if i in cur_dict.keys():
                    recall+=1

            fscore += 1.0/float((len(ansdict.keys())/float(precision) + len(ansdict.keys())/float(recall)))
        scores = (key,fscore)
    return scores

def calculate_score(uinput, para):
    global limit
    scores = []
    uinput = [uinput.lower().split()]
    cur_ngramsdict = ngrams(uinput) 
    print(cur_ngramsdict)
    para = cleanLines(para)
    ngramsdict = ngrams(para)
    fscore = 0.0
    for i in range(len(cur_ngramsdict)):
        cur_dict = cur_ngramsdict[i]
        ansdict = ngramsdict[i]
        
        precision = 0
        for i in cur_dict.keys():
            if i in ansdict.keys():
                precision+=1
                
        recall = 0
        for i in ansdict.keys():
            if i in cur_dict.keys():
                recall+=1
            
        fscore += 1.0/float((len(ansdict.keys())/float(precision) + len(ansdict.keys())/float(recall)))
    scores = [(fscore)]
    return scores