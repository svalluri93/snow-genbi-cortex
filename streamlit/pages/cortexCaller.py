from snowflake.cortex import Complete

class CortexCaller:

   def call_complete(_self,input):
      response = Complete('llama2-70b-chat', input)
      return response


   