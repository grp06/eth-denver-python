from django.shortcuts import render
#from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
#from langchain import OpenAI

#from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor
#from IPython.display import Markdown, display
#from llama_index import Document
#from langchain import OpenAI
#import os

from django.contrib.auth.models import User, Group
from .models import Company, Query
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, CompanySerializer, QuerySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

class QueryViewSet(viewsets.ModelViewSet):
    queryset = Query.objects.all()
    serializer_class = QuerySerializer
    permission_classes = [permissions.IsAuthenticated]



# max_input_size = 3700
# num_outputs = 300
# llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.5, model_name="text-davinci-003", max_tokens=num_outputs))
# prompt_helper = PromptHelper.from_llm_predictor(llm_predictor)

# def construct_index(directory_path, index_name):
#   documents = SimpleDirectoryReader(directory_path, recursive=True).load_data()
#   index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)
#   index.save_to_disk(index_name)
#   return index

# construct_index('./training-data', 'index_new.json')




# My OpenAI Key

# def buildIndex(text):
#     print("Building index...")
#     document = Document(text=text)
#     index = GPTSimpleVectorIndex([])
#     index.insert(document)
#     return index


# @app.route('/build-index', methods=['POST'])
# def build_index():
#     if 'file' not in request.files:
#         return 'No file uploaded'

#     # Read the file data from the request
#     file = request.files['file'].read()
#     file_extension = request.files['file'].filename.split('.')[-1]

#     # Parse the file to extract text
#     if file_extension == 'pdf':
#         with io.BytesIO(file) as pdf_file:
#             reader = PdfReader(pdf_file)
#             text = ''
#             for page in reader.pages:
#                 text += page.extract_text()
#     elif file_extension == 'txt':
#         text = file.decode('utf-8')
#     elif file_extension == 'md':
#         text = file.decode('utf-8')       
#     else:
#         return 'Unsupported file type'

#     # Call your buildIndex function with the extracted text
#     index = buildIndex(text)
#     # Serialize the entire index
#     index_str = index.save_to_string()
#     # Return the serialized index as a JSON object
#     return json.dumps({'index': index_str}) 