formats reddit comments in form of Q and A for gpt-2 like [so](https://openai.com/blog/better-language-models/#task1).
basically, we want something like this:

```
[some context]

Q: [question]
A: [response]

Q: [question]
A: [response]
```

you can run this in docker. make sure you have include a valid `usersim/praw.ini`.

`docker build -t reddit_gpt2_training:0.1 .`

`docker run -v output:/usersim/output reddit_gpt2_training:0.1 -user spez -num-comments 1000`


(outdated) here's a [colab notebook](https://colab.research.google.com/drive/1Kux-ZetSsfxdUhlLoCvmSAZy1WReLFRg) training and infering on reddit users' responses.
