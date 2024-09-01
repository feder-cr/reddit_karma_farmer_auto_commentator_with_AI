import praw
from random import randint, uniform
from time import sleep
from praw.exceptions import RedditAPIException
from generator_comment import GeneratorCommentGPT
import config_secrets

reddit = praw.Reddit(
    client_id=config_secrets.REDDIT_CLIENT_ID,
    client_secret=config_secrets.REDDIT_CLIENT_SECRET,
    username=config_secrets.REDDIT_USERNAME,
    password=config_secrets.REDDIT_PASSWORD,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
)

def get_trending_topics(reddit, commented_posts):
    trending_topics = []
    for submission in reddit.subreddit("all").hot(limit=500):
        if submission.id not in commented_posts:
            trending_topics.append(submission)
    return trending_topics

def extract_text_title(submission):
    return submission.title

def extract_text_content(submission):
    return submission.selftext

def extract_comment_content_and_upvotes(submission):
    submission.comments.replace_more(limit=0)
    comments = submission.comments.list()
    return [(comment.body, comment.score) for comment in comments]

def generate_comment(chat_llm, title, post_text, comments):
    try:
        return chat_llm.generate_comment(title, post_text, comments)
    except Exception as e:
        print(f"Error generating comment: {e}")
        return ""

def get_commented_posts(reddit):
    commented_posts = set()
    try:
        for comment in reddit.user.me().comments.new(limit=1000):
            commented_posts.add(comment.submission.id)
    except Exception as e:
        print(f"Error retrieving comments: {e}")
    return commented_posts

def pause_randomly():
    sleep_duration = uniform(4 * 60, 10 * 60)
    sleep(sleep_duration)

def delete_negative_comments(reddit):
    try:
        for comment in reddit.user.me().comments.new(limit=None):
            if comment.score < 0:
                print(f"Deleting comment with ID {comment.id} and score {comment.score}")
                comment.delete()
    except Exception as e:
        print(f"Error deleting comments: {e}")

def main():
    commented_posts = get_commented_posts(reddit)
    trending_topics = get_trending_topics(reddit, commented_posts)
    generator_post = GeneratorCommentGPT(openai_api_key=config_secrets.OPENAI_API_KEY)
    with open("commented_post_links.txt", "a") as file:
        for submission in trending_topics:
            post_title = extract_text_title(submission)
            text_content = extract_text_content(submission)
            comment_content_and_upvotes = extract_comment_content_and_upvotes(submission)
            comment = generate_comment(generator_post, post_title, text_content, comment_content_and_upvotes)
            if not comment:
                print(f"Skipping submission '{submission.title}' due to comment generation error.")
                continue
            exit = False
            while not exit:
                try:
                    response = submission.reply(comment)
                    # Write the URL of the commented post to the file
                    file.write(f"{response.submission.url}\n")
                    exit = True
                except RedditAPIException as e:
                    if e.error_type == "RATELIMIT":
                        sleep(int(e.message.split(" ")[-5]) * 60)
                    elif e.error_type == "THREAD_LOCKED":
                        print("Thread locked. Skipping.")
                        exit = True
                    else:
                        print(e.error_type)
                        exit = True
            print(f"Replied to '{submission.title}' with '{comment}'")
            commented_posts.add(submission.id)
            if randint(1, 30) == 1:
                pause_randomly()
                delete_negative_comments(reddit)
            else:
                sleep(randint(10, 400))

if __name__ == "__main__":
    main()
