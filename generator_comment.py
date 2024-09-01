from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import random

class GeneratorCommentGPT:
    def __init__(self, openai_api_key, model_name="gpt-4o-mini"):
        self.llm = ChatOpenAI(model_name=model_name, openai_api_key=openai_api_key)

    def _preprocess_template_string(self, template_string: str) -> str:
        return template_string

    def generate_comment(self, title: str, post_text: str, comments: list[tuple[str, int]]) -> str:
        # Primo template del prompt
        prompt_template_1 = """
        Title: {title}
        Text: {post_text}
        Comments: {comments}

        The post you are commenting on may fall into various categories. To maximize engagement and upvotes, follow these guidelines to craft a funny comment:

        1. **Analyze Successful Comments**:
        - use patterns or common elements in comments that received high engagement and positive responses.
        - Use insights from your knowlgment successful comments to guide your writing.

        2. **Tailor Your Comment Based on Post Type**:
        - **Funny Posts**: Add humor with witty observations, jokes, or amusing anecdotes. Use at most one emoji if appropriate to enhance the comedic effect.

        3. **General Tips for Creating Effective Comments**:
        - Craft unique and standout comments that offer genuine engagement. Avoid generic responses.
        - Engage directly with the post’s content to show understanding and interest.
        - Pose open-ended questions or invite others to share their perspectives to encourage interaction.
        - Ensure your tone is respectful and your comment adds value to the conversation.

        Your goal is to create a comment that not only resonates with the post but is also funny and creative. Ensure your comment is thoughtful, engaging, and tailored to fit the context of the post.
        Note: Comments should be funny, between 5 and 20 words, without quotation marks at the beginning and end, and include at most one emoji.
        """
        prompt_template_2 = """
        Title: {title}
        Text: {post_text}
        Comments: {comments}

        To create a highly engaging and funny comment, consider the following steps:

        1. **Leverage Trending Humor**:
        - Use memes, trending jokes, or cultural references to make your comment stand out.
        - Identify popular phrases or patterns that resonate with the community.

        2. **Adapt to the Post's Mood**:
        - **Lighthearted Posts**: Respond with puns, playful language, or clever one-liners. Use an emoji for emphasis, if necessary.
        - **Discussion Posts**: Introduce humor subtly, perhaps through irony or witty observations.

        3. **Comment Crafting Tips**:
        - Be concise and to the point. Humor is most effective when it’s sharp and succinct.
        - Engage with the content in a way that adds value or provokes thought.
        - Don’t be afraid to take risks, but ensure your comment remains respectful and within community guidelines.

        Your goal is to post a comment that is humorous, memorable, and contributes to the conversation. Keep it brief, engaging, and aligned with the post's tone. Comments should be funny, 5 to 20 words, and include a maximum of one emoji if relevant.
        Note: Comments should be funny, between 5 and 29 words, without quotation marks at the beginning and end, and include at most one emoji.
        """
        prompt_template_3 = """
        Title: {title}
        Text: {post_text}
        Comments: {comments}

        When crafting a comment that grabs attention and sparks interaction, consider asking engaging questions. Here’s how:

        1. **Question-Based Humor**:
        - Use a humorous question to make people think and laugh at the same time. Example: "Is this the best meme I've seen today or is it just me? 😂"
        - Posing a funny dilemma or hypothetical situation can also work well.

        2. **Engage with the Post**:
        - Ask a question that reflects on the content of the post. For example, "Why do I feel like this post is calling me out? 😅"
        - Create playful interactions by inviting others to answer or share their experiences.

        3. **Use Rhetorical Questions**:
        - A rhetorical question can add humor and make your comment stand out. Example: "Who needs sleep when you have posts like this, right?"

        Your goal is to create a comment that invites engagement through humor and curiosity. Ensure your comment is funny, between 5 and 20 words, and includes at most one emoji if needed.
        Note: Comments should be funny, between 5 and 27 words, without quotation marks at the beginning and end, and include at most one emoji.
        """
        prompt_template_1 = self._preprocess_template_string(prompt_template_1)
        prompt_template_2 = self._preprocess_template_string(prompt_template_2)
        prompt_template_3 = self._preprocess_template_string(prompt_template_3)
        selected_prompt_template = random.choice([prompt_template_1, prompt_template_2, prompt_template_3])
        prompt = ChatPromptTemplate.from_template(selected_prompt_template)
        chain = prompt | self.llm | StrOutputParser()
        output = chain.invoke({
            "title": title,
            "post_text": post_text,
            "comments": comments
        })
        return output
