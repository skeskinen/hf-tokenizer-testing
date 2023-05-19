import glob
from transformers import AutoTokenizer

tokenizer_names = ["EleutherAI/gpt-neox-20b", "bigscience/bloom-560m",
                   'gpt2-large', 'huggyllama/llama-7b', 'openlm-research/open_llama_7b_400bt_preview',
                   'bigcode/starcoder', 'EleutherAI/polyglot-ko-5.8b', 'facebook/galactica-6.7b']

file_paths = glob.glob("QQQ_*.txt")
testcases = []
for path in sorted(file_paths):
    with open(path, "r") as file:
        testcases.append(file.read())

# Initialize results list
results = []

# Loop through tokenizers
for tokenizer_name in tokenizer_names:
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    vocab_size = tokenizer.vocab_size

    # Initialize lists for pass_fail and tokenized_length
    pass_fail = []
    tokenized_length = []

    # Encode and decode each testcase
    for testcase in testcases:
        # Encode
        encoded = tokenizer.encode(testcase, add_special_tokens=False)
        tokenized_length.append(len(encoded))

        # Decode
        decoded = tokenizer.decode(encoded)
        pass_fail.append(decoded == testcase)

    # Store test results in results list
    results.append({
        "name": tokenizer_name,
        "vocab_size": vocab_size,
        "pass_fail": pass_fail,
        "tokenized_length": tokenized_length
    })

# Sort results by vocab size
results = sorted(results, key=lambda x: x["vocab_size"])

# Output results in a Markdown table
print("| Tokenizer Name | Vocab Size |", end="")
for i, _ in enumerate(testcases):
    print(f" QQQ_{i} |", end="")
for i, _ in enumerate(testcases):
    print(f" QQQ_{i} |", end="")
print()

print("|---|---|", end="")
for _ in testcases:
    print("---|---|", end="")
print()

for result in results:
    print(f"| {result['name']} | {result['vocab_size']} |", end="")
    for pf in result['pass_fail']:
        if pf:
            print(" ✔️ |", end="")
        else:
            print(" ❌ |", end="")
    for length in result['tokenized_length']:
        print(f" {length} |", end="")
    print()
