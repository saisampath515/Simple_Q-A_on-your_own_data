import streamlit as st
import base64
import os
import asyncio
from google import genai
from dotenv import load_dotenv
load_dotenv()
from google.genai import types
import base64
import nest_asyncio
from vector_store_creation import vector_creation

nest_asyncio.apply()  #Crucial: Apply nest_asyncio

# Replace with your actual API key or load from environment
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")

async def generate_content_async(user_input):
    """Asynchronous function to generate content using Gemini."""
    try:
        client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
        )
        model = "gemini-2.0-flash"
        contents = []

        contents.append(types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=user_input
                ),
            ],
        ),)

        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_mime_type="text/plain",
            system_instruction=[
            types.Part.from_text(
                text="""Hey you are a friendly model helps user's by answering using the context provided by the user."""
            ),
        ]
        )

        response=client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config,
        )
        contents.append(types.Content(
                role="model",
                parts=[
                    types.Part.from_text(
                        text=response.text
                    ),
                ],
            ))
        print(response.text, end="")
        return response.text
    except Exception as e:
        st.error(f"Error generating content: {e}")
        return None


async def main():
    st.title("Q&A on your data")

    uploaded_files = st.text_input(label="Provide the URL",placeholder="Provide the question for image uploaded")
    if uploaded_files:
        # for uploaded_file in uploaded_files:
        # bytes_data = uploaded_file.read()
        # from io import BytesIO
        # pdf_stream = BytesIO(bytes_data)
        # base64_data = base64.b64encode(bytes_data)
        # base64_string = base64_data.decode('utf-8')
        # print("PDF uploaded!!")
        raw_string = r"{}".format(uploaded_files) 
        vector_store=vector_creation(raw_string)
        # st.image(bytes_data, caption=f"Uploaded Image: {uploaded_file.name}", use_container_width=True)
        title = st.text_input(label="Question",placeholder="Provide the question for image uploaded")
        # st.write("The current movie title is", title)
        print(title)

        if st.button(f"Explain Image: {uploaded_files}"):
            with st.spinner(f"Generating explanation for {uploaded_files}..."):
                results = vector_store.similarity_search(
                    title,
                    k=2,

                )
                print(results)
                context=""
                for res in results:
                    print(f"* {res.page_content} [{res.metadata}]")
                    context+=f"* {res.page_content} \n[{res.metadata}\n\n"
                prompt=f"""Here is the context:{context}
                Here is the user question {title}"""
                response_text = await generate_content_async(prompt)
                if response_text:
                    st.write("Explanation:")
                    st.write(response_text)
                else:
                    st.error("Failed to generate explanation.")


if __name__ == "__main__":
    asyncio.run(main())