import math
import nltk
from nltk.corpus import wordnet
import language_tool_python

# Ensure NLTK data is downloaded
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

def evaluate_prompt_detailed(prompt, stats):
    # Complexity: Based on linguistic complexity
    complexity = lexical_diversity(prompt) + syntactic_complexity(prompt)

    # Efficiency: Output quality vs. prompt length
    efficiency = calculate_efficiency(prompt)

    # Compatibility: Based on alignment with bot stats
    compatibility = calculate_compatibility(prompt, stats)

    return {
        'complexity': complexity,
        'efficiency': efficiency,
        'compatibility': compatibility
    }

# Modify evaluate_prompt to use evaluate_prompt_detailed
def evaluate_prompt(prompt, stats):
    scores = evaluate_prompt_detailed(prompt, stats)
    # Composite score
    score = (scores['complexity'] * 0.3) + (scores['efficiency'] * 0.3) + (scores['compatibility'] * 0.4)
    return score

def lexical_diversity(prompt):
    tokens = nltk.word_tokenize(prompt)
    vocab = set(tokens)
    diversity = len(vocab) / len(tokens) if tokens else 0
    return diversity

def syntactic_complexity(prompt):
    sentences = nltk.sent_tokenize(prompt)
    words = nltk.word_tokenize(prompt)
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    return avg_sentence_length / 20  # Normalize

def calculate_efficiency(prompt):
    # Use language tool to check for grammar mistakes
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(prompt)
    num_errors = len(matches)
    efficiency = 1 / (num_errors + 1)
    return efficiency

def calculate_compatibility(prompt, stats):
    # Check for keywords related to bot's strengths
    keywords = {
        'Strength': ['powerful', 'smash', 'crush', 'strike', 'strong'],
        'Agility': ['quick', 'nimble', 'dodge', 'evade', 'swift'],
        'Intelligence': ['analyze', 'predict', 'strategy', 'outsmart', 'calculate'],
        'Defense': ['block', 'shield', 'guard', 'defend', 'absorb']
    }
    compatibility_score = 0
    for stat, words in keywords.items():
        if any(word in prompt.lower() for word in words):
            compatibility_score += stats.get(stat, 0) / 25  # Normalize stat
    return compatibility_score / len(keywords)  # Average compatibility
