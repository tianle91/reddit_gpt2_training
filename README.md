# Parsing and learning user comments.

formats reddit comments in form of Q and A for gpt-2 like [so](https://openai.com/blog/better-language-models/#task1).
basically, we want something like this:

```
[submission_text]
<u/other_reddit_user_0>: [comment]
<u/other_reddit_user_1>: [comment]
<u/target_user>: [comment]
```

You can run this in docker. make sure you have include a valid `usersim/praw.ini`.

```
docker build -t reddit_user_scraper .
docker run -v /path/to/output:/output reddit_user_scraper -user spez -num-comments 1000
```

Here's a [colab notebook](https://colab.research.google.com/drive/1AvgK26CPFYFJi6QFRjrpXxwY2DallQL5) where you can scrape `/u/spez` comments and interrogate him using `gpt_2_simple` by fine-tuning a pre-trained language model.
