import streamlit as st
from snowflake.snowpark import Session
from cortexCaller import call_complete
import snowflake.permissions as permission

st.title('Investintel', anchor=False)

class Dashboard:
   
    def __init__(self, session: Session) -> None:
        self.session = session

    def setup(self):
        st.header("Privileges setup")
        st.caption("""
         Follow the instructions below to set up your application.
         Once you have completed the steps, you will be able to continue to the main example.
      """)
        privilege = 'IMPORTED PRIVILEGES ON SNOWFLAKE DB'
        if not permission.get_held_account_privileges([privilege]):
            st.button(f"Grant import privileges on snowflake DB ↗", on_click=permission.request_account_privileges, args=[[privilege]], key='IMPORTED PRIVILEGES ON SNOWFLAKE DB')
        else:
            st.session_state.privileges_granted = True
            st.rerun()

    def run_streamlit(self):
        if not permission.get_held_account_privileges(['IMPORTED PRIVILEGES ON SNOWFLAKE DB']):
            del st.session_state.privileges_granted
            st.rerun()
       
        instructions = "Be concise. Do not hallucinate"

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {
                    'role': 'assistant',
                    'content': 'how can I help?'
                }
            ]

        for message in st.session_state.messages:
            with st.chat_message(message['role']):
                st.markdown(message['content'])


        prompt = st.chat_input("Type your message")

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
        
            with st.chat_message("user"):
                st.markdown(prompt)
            
            with st.chat_message("assistant"):  
                context = ",".join(f"role:{message['role']} content:{message['content']}" for message in st.session_state.messages)
                #response = Complete(model, f"Instructions:{instructions}, Context:{context}, Prompt:{prompt}") 
                input = f"Instructions:{instructions}, Context:{context}, Prompt:{prompt}"
                response = call_complete(input)
                st.markdown(response)
            
                st.session_state.messages.append({
                    'role': 'assistant',
                    'content': response
                })



if __name__ == '__main__':
   if 'privileges_granted' not in st.session_state:
      Dashboard(Session.builder.getOrCreate()).setup()
   else:
      Dashboard(Session.builder.getOrCreate()).run_streamlit()