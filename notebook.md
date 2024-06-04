```python
import os
import getpass

os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter Your OpenAI API Key:")
```

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.evaluation import load_evaluator

embedding_function = OpenAIEmbeddings()
evaluator = load_evaluator("pairwise_embedding_distance")

words = ("apple", "banana")
x = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[1])
print(f"Comparing ({words[0]}, {words[1]}): {x}")

words = ("apple", "iphone")
x = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[1])
print(f"Comparing ({words[0]}, {words[1]}): {x}")

words = ("apple", "apple")
x = evaluator.evaluate_string_pairs(prediction=words[0], prediction_b=words[1])
print(f"Comparing ({words[0]}, {words[1]}): {x}")
```

    Comparing (apple, banana): {'score': 0.09725941975023544}
    Comparing (apple, iphone): {'score': 0.09710853291781563}
    Comparing (apple, apple): {'score': -1.1102230246251565e-15}

```python
!python project.py sapiens.pdf 
```

    Split 1 documents into 111 chunks.
    The
    
    Present
    
    Humans transcend the boundaries of planet Earth. Nuclear weapons
    
    threaten the survival of humankind. Organisms are increasingly shaped
    
    by intelligent design rather than natural selection.
    
    The
    
    Intelligent design becomes the basic principle of life? Homo sapiens is
    
    Future
    
    replaced by superhumans?
    
    Part One
    
    The Cognitive Revolution
    
    1. A human handprint made about 30,000 years ago, on the wall of the Chauvet-Pont-d’Arc Cave in
    {'source': 'data/books/sapiens.pdf', 'start_index': 4136}
    Saved 111 chunks to chroma.

```python
!python main.py  "Why humans run the world?"
```

    0.7525280143990998
    Human: 
    Answer the question based only on the following context:
    
    We assume that a large brain, the use of tools, superior learning abilities and complex social structures are huge advantages. It seems self-evident that these have made humankind the most powerful animal on earth. But humans enjoyed all of these advantages for a full 2 million years during which they remained weak and marginal creatures. Thus humans who lived a million years ago, despite their big brains and sharp stone tools, dwelt in constant fear of predators, rarely hunted large game, and
    
    ---
    
    What was the Sapiens’ secret of success? How did we manage to settle so rapidly in so many distant and ecologically di(cid:643)erent habitats? How did we push all other human species into oblivion? Why couldn’t even the strong, brainy, cold- proof Neanderthals survive our onslaught? The debate continues to rage. The most likely answer is the very thing that makes the debate possible: Homo sapiens conquered the world thanks above all to its unique language.
    
    ---
    
    Today our big brains pay o(cid:643) nicely, because we can produce cars and guns that enable us to move much faster than chimps, and shoot them from a safe distance instead of wrestling. But cars and guns are a recent phenomenon. For more than 2 million years, human neural networks kept growing and growing, but apart from some (cid:635)int knives and pointed sticks, humans had precious little to show for it.
    
    ---
    
    Answer the question based on the above context: Why humans run the world?
    
    Response: content='Humans run the world thanks to their unique language, which allowed them to conquer the world and push other human species into oblivion.' response_metadata={'token_usage': {'completion_tokens': 26, 'prompt_tokens': 328, 'total_tokens': 354}, 'model_name': 'gpt-3.5-turbo', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None} id='run-55f25c47-24af-4277-bc01-c48362cff110-0' usage_metadata={'input_tokens': 328, 'output_tokens': 26, 'total_tokens': 354}
    Sources: ['data/books/sapiens.pdf', 'data/books/sapiens.pdf', 'data/books/sapiens.pdf']
