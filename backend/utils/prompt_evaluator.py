# backend/utils/prompt_evaluator.py

import nltk
from nltk.corpus import wordnet
import language_tool_python

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

def evaluate_prompt_detailed(prompt, stats):
    complexity = lexical_diversity(prompt) + syntactic_complexity(prompt)
    efficiency = calculate_efficiency(prompt)
    compatibility = calculate_compatibility(prompt, stats)

    return {
        'complexity': complexity,
        'efficiency': efficiency,
        'compatibility': compatibility
    }

def evaluate_prompt(prompt, stats):
    scores = evaluate_prompt_detailed(prompt, stats)
    score = (scores['complexity'] * 0.3) + (scores['efficiency'] * 0.3) + (scores['compatibility'] * 0.4)
    return score

def lexical_diversity(prompt):
    tokens = nltk.word_tokenize(prompt.lower())
    return len(set(tokens)) / len(tokens) if tokens else 0

def syntactic_complexity(prompt):
    sentences = nltk.sent_tokenize(prompt)
    words = nltk.word_tokenize(prompt)
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    return min(avg_sentence_length / 20, 1)  # Normalize and cap at 1

def calculate_efficiency(prompt):
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(prompt)
    num_errors = len(matches)
    return 1 / (num_errors + 1)  # Efficiency decreases with more errors

def calculate_compatibility(prompt, stats):
    keywords = {
        'Strength': ['powerful', 'smash', 'crush', 'strike', 'strong'],
        'Agility': ['quick', 'nimble', 'dodge', 'evade', 'swift'],
        'Intelligence': ['analyze', 'predict', 'strategy', 'outsmart', 'calculate'],
        'Defense': ['block', 'shield', 'guard', 'defend', 'absorb']
    }
    prompt_lower = prompt.lower()
    compatibility_score = sum(
        stats.get(stat, 0) / 25 for stat, words in keywords.items()
        if any(word in prompt_lower for word in words)
    )
    return compatibility_score / len(keywords)
