#Contains functions for getting cos_similarity scores and behavior/risk correlation scores

import gensim

"""
Sexual Harrassment
References:

    https://www.goodtherapy.org/learn-about-therapy/issues/sexual-abuse
    https://www.ptsd.va.gov/public/ptsd-overview/basics/symptoms_of_ptsd.asp
    http://www.mayoclinic.org/diseases-conditions/personality-disorders/symptoms-causes/dxc-20247656
---------
Bullying
References:

    https://www.burltwpsch.org/uploads/17/files/Characteristics%20of%20Bullies(1).pdf
    http://www.webmd.com/parenting/tc/bullying-characteristics-of-children-who-bully
---------
Drug abuse
References:

   http://www.webmd.com/mental-health/addiction/signs-of-drug-addiction#1
   http://www.mayoclinic.org/diseases-conditions/drug-addiction/basics/symptoms/con-20020970
"""

SH_victim_symptoms = ['depression', 'anger', 'anxiety', 'self-harm', 'unexplained fear', 'acting out',
           'nightmares', 'eating disorders', 'addiction to substances', 'trouble concentrating',
           'tough time sleeping', 'hostility', 'prefer to be alone', 'drug use', 'alcohol use', 'unsocial',
           'poor sleep']
D_user_symptoms = ['bloodshot eyes', 'bloody noses', 'lack motivation', 'irritability', 'agitation',
              'shakes', 'slurred speech', 'unhygenic', 'dirty', 'asking for money', 'weight gain',
              'weight loss', 'drop in grades', 'tired', 'spending too much money']
B_perp_symptoms = ['aggressive household', 'hit', 'push', 'trouble with rules', 'troublemaker',
                   'lack empathy', 'drug use', 'poor academic performance']
B_victim_symptoms = ['sensitive', 'anxiety', 'unsocial', 'prefer to be alone', 'depression',
                     'poor sleep']
all_dict = {'Sexual Harassment Victim': SH_victim_symptoms,
            'Drug Abuse Victim': D_user_symptoms,
            'Bullying Victim': B_victim_symptoms,
            'Bullying Perpetrator': B_perp_symptoms}

model_path = 'text.bin'

# this:          returns a list with n tuples of (similar_word, cos_similarity) pairs
# unknown_word:  word that is not in the dictionary
# dictionary:    one of the dictionaries from C1-C8
# top_n:         choose top N similar words
# model:         model from the load_model() method
def cos_max_word(unknown_word, dictionary, top_n, model):
    similarity = dict()

    for word in dictionary:
        if word in model.vocab:
            cos_similarity = model.similarity(word, unknown_word)
            similarity.update({word: cos_similarity})

    # sorts the cos similarity in decreasing order
    ordered_words = sorted(similarity.items(), key=lambda x: x[1], reverse=True)
    return ordered_words[:top_n]

# this:          returns a word2vec model
# model_path:    path to the text.model.bin file
def load_model(model_path):
    #return word2vec.Word2Vec.load_word2vec_format(model_path, binary=True)
    return gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)


def cos_score(user_in):
    """return the cosine simlarity score"""
    my_model = load_model(model_path)
    output = {}
    for d_key in all_dict.keys():
        #print(d_key)
        d = all_dict.get(d_key)
        cum = 0
        for word in user_in:
        #    print(word)
            if word in d:
                # pass  # return tf-idf score
                sc = 1
            else:
                # pass  # cos_similarity
                sc = cos_max_word(unknown_word=word, dictionary=d, top_n=1, model=my_model)[0][1]
        #        print(sc)
            cum += sc
        output[d_key] = cum
    #print(output)
    return sorted(output.items(), key=lambda x: x[1], reverse=True)


def corr_score(user_in):
    """return risk/behavior correlations score"""
    pass


#return combination score (cos_score * corr_score)
def get_score(user_in):
    """return the risk scores based on cos_similarity and risk/behavior correlations"""
    pass
