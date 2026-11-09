# Model Card: Mood Machine

I compared the two versions: the rule based model in `mood_analyzer.py` and the machine learning model in `ml_experiments.py`. The numbers below are from the runs I actually did.

## 1. Model Overview

**Model type:**  
I compared the two models. I used the same 14 posts for each of them.

**Intended purpose:**  
The model tries to label a short post as positive, negative, neutral, or mixed. It is a class exercise for seeing where a simple mood guesser breaks. It is not for judging real people, grading anyone, or reading private messages.

**How it works (brief):**  
The rule model lowercases the text, splits it into words and a few emoji, then adds one point for a positive word and subtracts one point for a negative word. If the word "not" (or a close word like "never" or "don't") comes right before a mood word, the point flips. A small set of emoji also adds or subtracts one point. The score is then turned into a label.  
The ML model counts how often each word appears and then learns which counts go with which label. I did not do any math by hand. I ran `python ml_experiments.py` and it trained on the posts and labels in `dataset.py`.

## 2. Data

**Dataset description:**  
`SAMPLE_POSTS` started with 6 posts. I added 8 more, so there are 14 posts and 14 labels. The new ones are a slang movie post with a laughing emoji, a sarcastic line about traffic, a stressed-but-proud exam post, a plain "just got home", mild praise about food, a tired post with a frown, a mixed line about a song, and "this party is sick" with a skull emoji.

**Labeling process:**  
I labeled each new post by the feeling I thought the writer meant, not by the cheerfulness of a single word. "not bad, the food was actually good" is positive because it is mild praise. "ugh I hate how good this song is" is mixed because it is annoyed and impressed at the same time. A few posts could honestly take another label. "I absolutely love getting stuck in traffic" looks positive if you trust the word "love", but I marked it negative because it is sarcasm. "this party is sick 💀" could mean the party is great or that it is awful. I marked it positive, as in slang for great. "not bad... actually good" could be read as only neutral. I marked it positive. I kept the original 6 labels, including "This is fine" as neutral, even though that phrase is sometimes a joke.

**Important characteristics of your dataset:**  

- Slang such as lowkey, fire, no cap, and sick
- Emoji such as 😂, :(, and 💀
- One sarcastic post
- Mixed feelings, including tired-but-hopeful, stressed-but-proud, and hate-how-good
- Very short posts with almost no mood words, such as "just got home" and "This is fine"
- Informal spelling, such as "im soooo tired rn"

**Possible issues with the dataset:**  
The set is tiny and uneven. Of the 14 labels, 5 are positive, 4 are negative, 3 are mixed, and only 2 are neutral. A lot of everyday words never appear. "hopeful" and "proud" are the good half of a mixed post, but they are not in the word list. One sarcastic example and one "sick" example are not enough to teach a pattern. The ML model is scored on these same 14 posts, so a perfect score can just mean it memorized them.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Each positive word adds 1. Each negative word subtracts 1. Repeated hits count again. The one enhancement I started with is negation: "not happy" subtracts 1, and "not bad" adds 1. The flip only looks at the very next word.  
After the breaker tests, I made one small extra change. Emoji-only lines were scoring 0. I gave :) , :-) , :D , ;) , and 😂 one positive point, and :( , :-( , and 😭 one negative point. I did not score 💀, because that mark is used in more than one way. I also did not add "sick" or "fire" to the word lists.  
Labels: if the positive side and the negative side showed up and the score is -1, 0, or 1, I call it mixed. If the score is above 0, positive. If it is below 0, negative. If it is 0 and only one side (or neither side) showed up, neutral. A score of 2 or more stays positive even if one negative word was present.

**Strengths of this approach:**  
Plain sentences that use the starter words behave the way I expect. "I love this class so much" is positive. "Today was a terrible day" is negative. "I am not happy about this" is negative because of the negation rule, and "not bad, the food was actually good" is positive for the same reason. "ugh I hate how good this song is" is mixed because hate and good cancel. "I love this class but I am so tired" is also mixed.

**Weaknesses of this approach:**  
It misses sarcasm. "I absolutely love getting stuck in traffic" is positive in the model and negative in my label, because it only sees "love". It misses slang that is not in the list. "this party is sick 💀", "that concert was sick", and "this burger is fire" all score 0 and come out neutral. It only sees one side of a mixed post when the other word is missing: "Feeling tired but kind of hopeful" and "kinda stressed about the exam but also proud I studied" comes out negative too. "not very happy about this" comes out positive, because "very" sits between "not" and "happy", so the flip never happens.

**Breaker tests, before and after the emoji change:**  
Before the emoji points, these lines all scored 0 and were labeled neutral: `:)` , `:(` , `😂` , "long day 😭", "had a blast :)", and "lowkey this movie was fire no cap 😂". After the change, the first three face marks and "long day 😭" and "had a blast :)" match the mood of the emoji, and the movie line is positive because of 😂, not because the model understands "fire". On the 14 labeled posts, that was the only label that changed. Accuracy went from 9 of 14 to 10 of 14. Sarcasm and the words sick and fire missed before the change and after it.

## 4. How the ML Model Works (if used)

**Features used:**  
Bag of words. `CountVectorizer` counts words and throws away punctuation and emoji. A post that is only `:)` or `😂` has no words left, so the model is guessing from the class starting scores. The negative class had the highest starting score in this run, so those emoji-only posts came out negative.

**Training data:**  
The model trained on `SAMPLE_POSTS` and `TRUE_LABELS`. `python ml_experiments.py` then tested those same 14 posts.

**Training behavior:**  
With all 14 posts, training accuracy was 1.00. That number moved when I changed the setup. Trained on only the original 6 posts, accuracy on those 6 was 1.00, but accuracy on the 8 posts I added later was 1 of 8 (0.12). The only new post it got right was "im soooo tired rn :(".  
It is sensitive to single labels. I flipped the traffic post from negative to positive and retrained. Training accuracy stayed 1.00, but the traffic post, "Yeah I love when my phone dies", and "I love waiting in traffic" all changed from negative to positive. "I love this class so much" stayed positive. When I deleted the traffic post instead, those sarcastic "love" lines went back to positive. Flipping "just got home" from neutral to negative changed that one post from neutral to negative and left "This is fine" neutral. One label can either stay local or pull nearby sentences with it, depending on whether the words are shared.

**Strengths and weaknesses:**  
On the 14 training posts it got every label, including the four the rule model missed. That is memorizing a tiny set, not proof it understands mood. Off that set it picks up stray cues. "happy" only appears in "I am not happy about this", so "I am happy" is predicted negative. "im" only appears in the tired post, so "im excited" is predicted negative even though "excited" is a positive word (the kept features were "excited" and "im"). "sick" and "fire" get a positive weight from one slang post each, so "I feel sick" and "the kitchen is on fire" are predicted positive. "but" gets a strong mixed weight, and "day" and "today" get a negative weight from "Today was a terrible day".

## 5. Evaluation

**How you evaluated the model:**  
I ran `python main.py` for the rule model and `python ml_experiments.py` for the ML model. The rule model accuracy on the 14 posts was **0.71** (10 correct, 4 wrong). The ML model accuracy on those same posts was **1.00** (14 of 14). The ML number is training accuracy. The same training code, fit on only the first 6 posts, got 1 of the other 8 right.

**Examples of correct predictions:**  

- "I am not happy about this" is negative in the rule model. The score is -1 from "not happy". The ML model also says negative on this training post.
- "not bad, the food was actually good" is positive in the rule model. "not bad" flips to a positive point and "good" adds another, for a score of 2.
- "ugh I hate how good this song is" is mixed in the two models. In the rule model, "hate" and "good" cancel to 0 and the two sides are present.
- "im soooo tired rn :(" is negative in the rule model. "tired" and the frown each subtract a point, score -2. Informal spelling around the word "tired" did not confuse it.

**Examples of incorrect predictions:**  

- Rule model: "Feeling tired but kind of hopeful" was predicted negative, true label mixed. The only listed word is "tired". "hopeful" is invisible, so the hopeful half never raises the score.
- Rule model: "I absolutely love getting stuck in traffic" was predicted positive, true label negative. The model sees "love" and has no way to tell that the praise is sarcastic. The ML model says negative on this exact training post, but if that post is removed and the model is retrained, it says positive too.
- Rule model: "kinda stressed about the exam but also proud I studied" was predicted negative, true label mixed. "stressed" is in the negative list and "proud" is not, so it only counts the stress.
- Rule model: "this party is sick 💀" was predicted neutral, true label positive. "sick" is not in either word list, and the skull emoji is not scored. The ML model says positive on this training post. On a new line, "I feel sick", the ML model also says positive, which is the wrong way to read feeling ill. The rule model says neutral there, which is still wrong, but it does not call illness a good mood.
- ML model on new text: "I am happy" was predicted negative. The rule model says positive. The only training post that contains "happy" is the negative sentence "I am not happy about this", so the ML model treats the word "happy" as a negative clue.
- ML model on new text: ":)" was predicted negative. The rule model says positive after the emoji fix. The ML vectorizer drops the emoji, and with no words left it falls to negative.
- ML model on new text: "I love this class but I am so tired" was predicted positive. The rule model says mixed, which matches the two feelings. The word "so" has a strong positive weight from posts like "So excited for the weekend".

## 6. Limitations

The dataset has 14 short posts, so I would not trust either model on a new topic or a longer message. The rule model cannot see sarcasm, and it cannot see a feeling whose word is missing from the list. Negation breaks when another word sits in the middle, as in "not very happy". The emoji list is short on purpose, and 💀 is still ignored. The ML model looks perfect only because it is tested on the posts it just memorized. With 6 training posts it got 1 of 8 new posts right. It will copy a one-off word: "happy" becomes negative, "im" becomes negative, and "sick" or "fire" becomes positive. Empty text and emoji-only text come out negative for the ML model because that class has the highest starting score. Neither version should be treated as a real mood detector.

## 7. Ethical Considerations

A wrong label can matter if someone acts on it. The rule model reads a sarcastic complaint ("I absolutely love getting stuck in traffic") as positive, so it can miss that the writer is annoyed. It reads "Feeling tired but kind of hopeful" as simply negative, so it drops the hopeful part. The ML model reads "I am happy" as negative and "I feel sick" as positive. Used on private messages, either mistake is a privacy problem as well as a wrong guess. I would not use these models to screen students, employees, or anyone who might be in distress. They are a lab demo.

**Overt bias:**  
The rule model underserves casual slang and nonstandard spelling. I checked the same mood in plain wording and in informal wording. "I love this class", "This is great", and "I am so excited" were positive. "i luv this class", "this is fire", and "im hype af" were neutral, because luv, fire, and hype are not in the word list. Informal writing that still uses a listed word did match: "I am very tired today" and "im soooo tired rn" were negative in each case. The gap is the vocabulary, not every shortcut in spelling. The ML model does not fix that gap. "i luv this class" came out positive only because "this" and "class" were in a positive training post, and "luv" was not even a feature. "im excited" came out negative. The features it kept were "excited" and "im", and "im" had picked up a negative weight from the single post "im soooo tired rn".

**Covert compliance:**  
My AI coding assistant agreed with the starter word lists and the plus-one, minus-one score. It did not push back on those lists or say they leave slang out. When the slang tests failed, it did not just add sick and fire to the positive list. It kept them out because sick also means ill, as in "I feel sick", and fire is not always praise, as in a real fire. It also left the skull emoji unscored, so "this party is sick 💀" stayed neutral. The only scoring change it made after the tests was the small emoji list, and only for faces that had scored zero.

## 8. Ideas for Improvement

I would add more labeled posts, and I would keep some of them out of training so the ML score is not just memory. I would add words I actually needed, such as hopeful and proud, and I would handle "sick" with context instead of one list, because praise and illness should not share a label. I would let negation skip a filler word like "very". I would give the ML model a way to see emoji, since right now `:)` and `😂` disappear. I would not trust a word that appears in only one post. "happy", "im", "sick", and "fire" all got their lean from a single example, and that lean was wrong on new sentences.
