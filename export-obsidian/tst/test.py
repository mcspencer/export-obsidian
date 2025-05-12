from langchain import LangChain
from langchain.llms import Bedrock
from langchain.output_parsers import OutputParser

# Initialize the LangChain application
langchain_app = LangChain()

# Configure Bedrock with Claude Haiku 3.5
llm = Bedrock(model="claude-haiku-3.5")

# Attach an output parser
output_parser = OutputParser()

# Set the LLM and output parser in the LangChain application
langchain_app.set_llm(llm)
langchain_app.set_output_parser(output_parser)

# Example function to test the setup
def test_langchain_app(input_text):
    response = langchain_app.generate(input_text)
    parsed_output = output_parser.parse(response)
    return parsed_output

# Test the LangChain application
if __name__ == "__main__":
    test_input = "Hello, how are you?"
    result = test_langchain_app(test_input)
    print(result)
