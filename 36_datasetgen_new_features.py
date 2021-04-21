# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 10:04:21 2020

@author: Pramod
"""
import email.parser 
import os, sys, stat,re,csv,datetime
import pandas as pd
from nltk import word_tokenize
from nltk.corpus import stopwords,words


file_counter=0
header_writer=0


def extract_email_id(str_mail_id):
    emai_id=dataclean(str(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",str(str_mail_id))))
    if(emai_id==""):
        emai_id="None" 
    return emai_id

def remove_stopwords_subject(sentence):
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(sentence)
    filtered_sentence = [str.lower(w) for w in word_tokens if not w in stop_words]
    for char in ",[]'":
            filtered_sentence=str(filtered_sentence).replace(char,"")

    return filtered_sentence
    
def dataclean(strtoremove):
    strtemp=str(strtoremove)
    for char in ",[]'<>():":
            strtemp=strtemp.replace(char,"")
    strtemp=strtemp.replace("\n","")
    return strtemp

def subject_probability(sub_line):
    prob=0
    c_spam_w=0
    c_tot_w=0
    file_not_eng_words = open('not_eng_words.txt','a') 
    for sub_line_word in sub_line.split():
        c_tot_w=len(sub_line.split())
        #dict_eng = enchant.Dict("en_US")
        #if(dict_eng.check(sub_line_word)):
        if(sub_line_word in words.words()):
            with open('spam_words.txt', 'r') as spam_file:
                for row in spam_file:
                    spam_word=row.rstrip("\n")
                    if spam_word==sub_line_word: 
                        c_spam_w+=1
                        break
                        #prob=float(c_spam_w)/float(c_tot_w)
        else:
            file_not_eng_words.write(sub_line_word+"\n")
            #print(sub_line_word)
            c_spam_w+=1
        prob=float(c_spam_w)/float(c_tot_w)
            
    return prob


      
def ExtractHeaders(filename):
    if not os.path.exists(filename):
        print ("ERROR: input file does not exist:", filename)
        os.exit(1)
    fp = open(filename,errors='ignore')
    print(filename+" "+str(file_counter))
    
#    global STP,STN,SFP,SFN,TOTAL_FILES,sub_accuracy
#    global IPTP,IPTN,IPFP,IPFN,IP_accuracy
#    global sender_TP,sender_TN,sender_FP,sender_FN,sender_accuracy
#    global spam_TP,spam_TN,spam_FP,spam_FN,spam_accuracy
        
    msg = email.message_from_file(fp)
    type_of_file=filename.find('spam',0,len(str(filename)))
    filetype= 0 if type_of_file==-1 else 1
        
    
    Subject=dataclean(msg.__getitem__("Subject"))
    Received_IP_Address=dataclean(re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(msg.get_all("Received"))))
    #sender_email_add=dataclean(extract_email_id(msg.__getitem__("From")))
    Received_IP_Address=dataclean(re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", str(msg.get_all("Received"))))
    From=dataclean(extract_email_id(msg.__getitem__("From")))
    No_of_Received_ip_add ="0" if Received_IP_Address=="None" else len(Received_IP_Address.split(" "))
        
    Reply_To ="0" if msg.__getitem__("Reply-To")== None else ""+ dataclean(str(msg.__getitem__("Reply-To")))
    No_Reply_To="0" if Reply_To=="None" else len(Reply_To.split(" "))
    Received_email_id=dataclean(extract_email_id(msg.get_all("Received")))
    No_Received_email_id=len(Received_email_id.split(" "))
    Delivered_To=dataclean(extract_email_id(msg.__getitem__("Delivered-To")))
    No_Delivered_To="0" if Delivered_To=="None" else len(Delivered_To.split(" "))
        
    To=dataclean(extract_email_id(msg.__getitem__("To")))
    Cc=dataclean(extract_email_id(msg.__getitem__("Cc")))
    Bcc=dataclean(extract_email_id(msg.__getitem__("Bcc")))
    No_of_To="0" if To=="None" else len(To.split(" "))
    No_of_Cc="0" if Cc=="None" else len(Cc.split(" "))
    No_of_Bcc="0" if Bcc=="None" else len(Bcc.split(" "))
    No_from="0" if From=="None" else len(From.split(" "))
    Return_path =dataclean(str(msg.__getitem__("Return-Path")))
    No_Return_path="0" if Return_path=="None" else len(Return_path.split(" "))
    Subject=dataclean(msg.__getitem__("Subject"))
    len_sub=len(Subject)
    filtered_subject=str(remove_stopwords_subject(Subject))
    subject_prob=subject_probability(str.lower(filtered_subject))
    
#    mail_body_clean=dataclean(msg.get_payload())
#    content_prob=subject_probability(str.lower(mail_body_clean))
    
    No_X_Mailer="0" if msg.__getitem__("X-Mailer")==None else "1"
#    Content_Length=msg.__getitem__("Content-Length")
#    len_content_calculated=len(str(msg.get_payload()))
    Lines=msg.__getitem__("Lines")
    len_headers=msg.__len__()
    msg_content_type=msg.get_content_maintype()

    email_df = pd.DataFrame({'filename':filename,
                             'len_headers':len_headers,
                             'len_sub':len_sub,
                             'subject_prob':subject_prob,
#                             'len_content_calculated':len_content_calculated,
#                             'content_prob':content_prob,
                             'msg_content_type':msg_content_type,
#                             'Content_Length':Content_Length,
                             'Lines':Lines,
                             'No_Delivered_To':No_Delivered_To,
                             'No_Reply_To':No_Reply_To,
                             'No_of_To':No_of_To,
                             'No_of_Cc':No_of_Cc,
                             'No_of_Bcc':No_of_Bcc,
                             'No_of_Received_ip_add':No_of_Received_ip_add,
                             'No_Received_email_id':No_Received_email_id,
                             'No_from':No_from,
                             'No_Return_path':No_Return_path,
                             'No_X_Mailer':No_X_Mailer,
                             'filetype': filetype},index=[0])
                                   
    if(file_counter==1):
        email_df.to_csv('Enron_Dataframe_new_features.csv',mode='a',index=False)  
    else:
        email_df.to_csv('Enron_Dataframe_new_features.csv',mode='a',header=False,index=False)
              
def ExtractHeaderFromFiles (srcdir):
    try:
        files = os.listdir(srcdir)
        global file_counter
        
        file_counter=0
     
        for file in files:
            file_counter+=1
            srcpath = os.path.join(srcdir, file)
            src_info = os.stat(srcpath)
            if stat.S_ISDIR(src_info.st_mode):
                ExtractHeaderFromFiles(srcpath)
            else:  
                ExtractHeaders (srcpath)
    except Exception as ve:
        print(srcpath)
        print(ve)
                        
###################################################################
#print ('Input source directory: ') #ask for source and dest dirs
#srcdir = input()
srcdir = "G:/Documents/Research/SPAM/2nd Six Monthly/Enron Dataset/DS"

#if os.path.exists("Extracted_data.csv") and os.path.exists("not_eng_words.txt"):
if os.path.exists("Enron_Dataframe_new_features.csv"):
    os.remove("Enron_Dataframe_new_features.csv")
    print("Enron_Dataframe_new_features.csv is removed")
               
if not os.path.exists(srcdir):
    print ('The source directory %s does not exist, exit...' % (srcdir))
    sys.exit()
###################################################################
TOTAL_FILES=0
start_time=datetime.datetime.now()
ExtractHeaderFromFiles(srcdir)
end_time=datetime.datetime.now()
print(end_time-start_time)


