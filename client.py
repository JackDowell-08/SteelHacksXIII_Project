import asyncio
from agents import agent
from IPython.display import Markdown as md


def ask_agent(user_topic):

    state = {"role" : "user", "content" : user_topic}

    state = agent.invoke(state)
    response = state['messages'][-1]

    summary = md(response.content)

    print(response.content)

    return summary


if __name__ == '__main__':
    ask_agent("I'm interested in Tesla (TSLA)")