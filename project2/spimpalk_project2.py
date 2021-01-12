#The linked list
class LinkedList:

    def __init__(self, index=0, mode="simple"):
        self.start_node = None # Head pointer
        self.end_node = None # Tail pointer
        # Additional attributes
        self.index = index 
        self.mode = "simple"

    # Method to traverse a created linked list
    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            print("List has no element")
            return
        else:
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                traversal.append(n.value)
                n = n.next
            return traversal

    # Method to insert elements in the linked list
    def insert_at_end(self, value):
        # determine data type of the value
        if 'list' in str(type(value)):
            self.mode = "list"

        # Initialze a linked list element of type "Node" 
        new_node = Node(value)
        n = self.start_node # Head pointer

        # If linked list is empty, insert element at head
        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return "Inserted"
        
        elif self.mode == "list":
            if self.start_node.value[self.index] >= value[self.index]:
                self.start_node = new_node
                self.start_node.next = n
                return "Inserted"

            elif self.end_node.value[self.index] <= value[self.index]:
                self.end_node.next = new_node
                self.end_node = new_node
                return "Inserted"

            else:
                while value[self.index] > n.value[self.index] and value[self.index] < self.end_node.value[self.index] and n.next is not None:
                    n = n.next

                m = self.start_node
                while m.next != n and m.next is not None:
                    m = m.next
                m.next = new_node
                new_node.next = n
                return "Inserted"
        else:
            # If element to be inserted has lower value than head, insert new element at head
            if self.start_node.value >= value:
                self.start_node = new_node
                self.start_node.next = n
                return "Inserted"

            # If element to be inserted has higher value than tail, insert new element at tail
            elif self.end_node.value <= value:
                self.end_node.next = new_node
                self.end_node = new_node
                return "Inserted"

            # If element to be inserted lies between head & tail, find the appropriate position to insert it
            else:
                while value > n.value and value < self.end_node.value and n.next is not None:
                    n = n.next

                m = self.start_node
                while m.next != n and m.next is not None:
                    m = m.next
                m.next = new_node
                new_node.next = n
                return "Inserted"
    
    # Method to intersect two linked lists    
    def intersection(self,llist):
        num_comparisons = 0
        intersect = LinkedList()
        n1 = self.start_node
        n2 = llist.start_node
        while(n1 is not None and n2 is not None):
            if(n1.value==n2.value):
                intersect.insert_at_end(n1.value)
                n1 = n1.next
                n2 = n2.next
                num_comparisons +=1
            elif(n1.value>n2.value):
                n2 = n2.next
                num_comparisons +=1
            elif(n1.value<n2.value):
                n1 = n1.next
                num_comparisons+=1
        return intersect,num_comparisons
        
# The data structure for every element in the linked list. 
class Node:
    def __init__(self, value = None, next = None):
        self.value = value
        self.next = next

import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer 
import json
import sys

nltk.download('stopwords')
REGEX_SPECIAL_CHARACTERS = r"[^a-zA-Z0-9]+"
stemmer = PorterStemmer()
token_dictionary = {}
posting_list_dict = {}
daat_list_dict = {}

def stopwords_stem_processing(line_list):
    stop_words = set(stopwords.words('english'))
    return [stemmer.stem(word) for word in line_list if not word in stop_words] 


def remove_special_char(line_data):
    return re.sub(REGEX_SPECIAL_CHARACTERS, ' ', line_data).strip()

def preprocess_line(line):
    line = line.strip().lower()
    line_array = line.split('\t')
    line_array[1] = remove_special_char(line_array[1]).split(' ')
    line_array[1] = stopwords_stem_processing(line_array[1])
    # print(line_array[1])
    return line_array

def create_posting_list(line):
    line[1] = set(line[1])
    for word in line[1]:
        if(word not in token_dictionary):
            token_dictionary[word] = LinkedList()
        token_dictionary[word].insert_at_end(int(line[0]))
    return True


def read_file(filename):
    with open(filename) as file:
        data = file.readlines()
    return data

def create_inverted_index(filename):
    data = read_file(filename)
    for line in data:
        preprocessed_line = preprocess_line(line)
        created = create_posting_list(preprocessed_line)
    
    return created

def preprocess_query(query):
    query = query.strip().lower()
    query = remove_special_char(query).split(' ')
    query = stopwords_stem_processing(query)
    return query


def get_posting_list(query_words):
    for word in query_words:
        word_llist = token_dictionary[word]
        posting_list_dict[word] = word_llist.traverse_list()
    return posting_list_dict

def get_daat_list(query_words,actual_query):
    total_comparisons = 0
    query_words_num = len(query_words)
    and_llist = token_dictionary[query_words[0]]
    for i in range(1,query_words_num):
        and_llist,num_comparisons = and_llist.intersection(token_dictionary[query_words[i]]) 
        total_comparisons+=num_comparisons
    and_list = and_llist.traverse_list() 
    daat_list_dict[actual_query.strip()] = {"results":and_list,
                                    "num_docs":len(and_list),
                                    "num_comparisons":total_comparisons
                                    }
    return daat_list_dict


def sort_by_token_len(query_data):
    query_data_list = []
    for word in set(query_data):
        query_data_list.append((word,len(posting_list_dict[word])))
    query_data_list.sort(key= lambda x: x[1])
    return [tup[0] for tup in query_data_list]


def read_queries(filename):
    result = {}
    queries = read_file(filename)
    for query in queries:
        preprocessed_query = preprocess_query(query) 
        result["postingsList"] = get_posting_list(preprocessed_query)
        preprocessed_query = sort_by_token_len(preprocessed_query)
        result["daatAnd"] = get_daat_list(preprocessed_query,query)
    return result

def write_json_to_file(filename,output):
    with open(filename,'w') as file:
        file.write(json.dumps(output))
    return True

if __name__ == "__main__":
    # Arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    query_file = sys.argv[3]
    
    #Functions
    create_inverted_index(input_file)   # To create inverted Index
    output = read_queries(query_file)   # To read queries file
    write_json_to_file(output_file,output)   # write output file