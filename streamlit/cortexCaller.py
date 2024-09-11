from snowflake.cortex import Complete

def call_complete(input):
   response = Complete('llama2-70b-chat', input)
   return response


   