#entitiy index detector formatted for training the NER data
def find_entity_indices(text, entity, label="ORG"):
    """
    Find all start indices of an entity in the given text.

    Args:
        text (str): The text to search within.
        entity (str): The entity to find.

    Returns:
        list: A list of starting indices where the entity is found in the text.
    """
    indices = []
    start = 0
    
    while start < len(text):
        start = text.find(entity, start)
        if start == -1:
            break
        end = start + len(entity)
        indices.append((start, end, label))
        start += 1  # Move past the current found entity
    
    return indices

# Example usage
text = """Hi Udall,
Thanks for applying to our 2025 Charles Schwab Model Risk Internship 
(Artificial Intelligence, Machine Learning, Financial Engineering and Data Science), 2024-101928.
Our Talent Acquisition teams are working through the many applications Schwab receives and will 
reach out if you are selected for an interview."""
entity = "Charles Schwab"
indices = find_entity_indices(text, entity)
print(indices)  # Output: [0, 45]