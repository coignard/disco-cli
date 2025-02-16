from typing import Dict, List

SKILL_CATEGORIES: Dict[str, List[str]] = {
    'INTELLECT': ['Logic', 'Encyclopedia', 'Rhetoric', 'Drama', 'Conceptualization', 'Visual Calculus'],
    'PSYCHE': ['Volition', 'Inland Empire', 'Empathy', 'Authority', 'Esprit De Corps', 'Suggestion'],
    'PHYSIQUE': ['Endurance', 'Pain Threshold', 'Physical Instrument', 'Electrochemistry', 'Shivers', 'Half Light'],
    'MOTORICS': ['Hand/Eye Coordination', 'Perception', 'Reaction Speed', 'Savoir Faire', 'Interfacing', 'Composure']
}

DIFFICULTY_LEVELS: Dict[str, range] = {
    'Trivial': range(6, 8),
    'Easy': range(8, 10),
    'Medium': range(10, 12),
    'Challenging': range(12, 13),
    'Formidable': range(13, 14),
    'Legendary': range(14, 15),
    'Heroic': range(15, 16),
    'Godly': range(16, 18),
    'Impossible': range(18, 21)
}

SKILL_COLORS: Dict[str, str] = {
    'INTELLECT': '#4DA6B3',
    'PSYCHE': '#624AB4',
    'PHYSIQUE': '#AE3C5C',
    'MOTORICS': '#C3A22B'
}
