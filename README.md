# hf-tokenizer-testing 

A simple script to test if tokenizers from various popular models can encode+decode documents losslessly.

Documents tested are:
* QQQ_0: Simple sanity test
* QQQ_1: A sample from TinyStories dataset that looks innocent, but most tokenizers seem to fail because of a little bit unusual punctuation.
* QQQ_2: Another, easier, sample from TinyStories
* QQQ_3: Markus Kuhn's UTF-8 stress test, with couple lines removed b/c python encoder couldn't handle them. Correctly encoding/decoding this document is a very good sign of "correctness".
* QQQ_4: Wikipedia page source for Snow Leopard
* QQQ_5: Book Pride and Prejudice from The Project Gutenberg
* QQQ_6: stb_image.h. C source code file
* QQQ_7: Japanese book from The Project Gutenberg, 苦悶の欄(Kumon no ran)

## Why?
Does it matter if tokenizers can/can't reproduce the input exactly? I guess this is subjective, but I'd say it's at least a nice feature. A feature that (perhaps surprisingly?) most tokenizers out there don't seem to have.

I wrote this for myself on a quest to find a tokenizer I like and I was kind of surprised by the results so I decided to share them.

## Results

| Tokenizer Name | Vocab Size | QQQ_0 | QQQ_1 | QQQ_2 | QQQ_3 | QQQ_4 | QQQ_5 | QQQ_6 | QQQ_7 | QQQ_0 | QQQ_1 | QQQ_2 | QQQ_3 | QQQ_4 | QQQ_5 | QQQ_6 | QQQ_7 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EleutherAI/polyglot-ko-5.8b | 30000 | ✔️ | ❌ | ✔️ | ❌ | ❌ | ✔️ | ❌ | ✔️ | 36 | 436 | 428 | 18310 | 292044 | 390318 | 197049 | 144043 |
| huggyllama/llama-7b | 32000 | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | 12 | 231 | 223 | 5465 | 187793 | 196813 | 115284 | 88333 |
| openlm-research/open_llama_7b_400bt_preview | 32000 | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | 30 | 225 | 218 | 15452 | 189579 | 197971 | 148109 | 210463 |
| bigcode/starcoder | 49152 | ✔️ | ❌ | ✔️ | ❌ | ❌ | ✔️ | ❌ | ✔️ | 11 | 240 | 240 | 4678 | 179713 | 206842 | 104817 | 72613 |
| facebook/galactica-6.7b | 50000 | ✔️ | ❌ | ✔️ | ❌ | ❌ | ✔️ | ❌ | ❌ | 11 | 248 | 236 | 5158 | 216860 | 196171 | 127599 | 145842 |
| EleutherAI/gpt-neox-20b | 50254 | ✔️ | ❌ | ✔️ | ❌ | ❌ | ✔️ | ❌ | ✔️ | 11 | 216 | 210 | 4897 | 167877 | 183997 | 106364 | 76410 |
| gpt2-large | 50257 | ✔️ | ❌ | ✔️ | ❌ | ❌ | ✔️ | ❌ | ✔️ | 28 | 217 | 213 | 14781 | 175021 | 196107 | 139985 | 99792 |
| bigscience/bloom-560m | 250680 | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | ✔️ | 10 | 230 | 210 | 4082 | 127679 | 182074 | 92153 | 66894 |

## My Takeaways
* Llama tokenizer is really good. Small vocab, lossless, good compression, shown to work well in a real LLM.
* Open Llama is ok in English but has drastically worse compression than Llama in the utf8 test and Japanese. In my opinion, this is a pretty bad look.
* Only other lossless tested here was bloom, but 250k vocab is kind of yucky for me. All the extra tokens lower the lengths a little bit, but is it worth it?
* All the other tokenizers seem to have serious trouble reprocuding punctuation. Personally, I think this is especially bad in the programming example. None of the other tokenizers could exactly reproduce the given C source file (including starcoder)

## Duplicates
Many models use the same tokenizers. Listing some of the relationships here for future reference to myself.
* gpt2: EleutherAI/gpt-j-6b, facebook/opt-66b (plus couple extra tokens), EleutherAI/gpt-neo-125m, roneneldan/TinyStories-8M
* EleutherAI/gpt-neox-20b: EleutherAI/pythia-2.8b, 