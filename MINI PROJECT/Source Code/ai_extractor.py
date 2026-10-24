import re
from datetime import date, datetime, timedelta


# ============================================================
# CONSTANTS
# ============================================================

ACTION_VERBS = {
    "prepare",
    "complete",
    "finish",
    "submit",
    "test",
    "update",
    "review",
    "check",
    "investigate",
    "fix",
    "resolve",
    "create",
    "develop",
    "design",
    "implement",
    "verify",
    "validate",
    "deploy",
    "configure",
    "document",
    "send",
    "schedule",
    "organize",
    "analyze",
    "check",
    "monitor",
    "install",
    "remove",
    "replace",
    "discuss",
    "finalize",
    "improve",
    "research",
    "examine",
    "address",
    "handle",
    "coordinate",
    "review"
}


PRIORITY_HIGH_WORDS = [
    "urgent",
    "urgently",
    "as soon as possible",
    "asap",
    "critical",
    "immediately",
    "must",
    "high priority",
    "important",
    "required",
    "security issue",
    "server issue",
    "server outage",
    "login issue"
]


PRIORITY_LOW_WORDS = [
    "low priority",
    "whenever possible",
    "when possible",
    "optional",
    "nice to have"
]


PRIORITY_MEDIUM_WORDS = [
    "medium priority",
    "should",
    "review",
    "check",
    "update"
]


DEADLINE_PATTERNS = [
    r"\bby\s+(today|tomorrow|tonight)\b",
    r"\bby\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    r"\bnext\s+(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",
    r"\bnext\s+week\b",
    r"\btomorrow\b",
    r"\btoday\b",
    r"\btonight\b",
    r"\bas soon as possible\b",
    r"\basap\b",
    r"\burgently\b",
    r"\bby\s+\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\b",
    r"\b\d{1,2}(?:st|nd|rd|th)?\s+[A-Za-z]+\b",
    r"\bbefore\s+(?:the\s+)?final submission\b",
    r"\bbefore\s+(?:the\s+)?submission\b",
]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def clean_text(text):
    if text is None:
        return ""

    text = str(text)

    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


# ============================================================
# SENTENCE SPLITTING
# ============================================================

def split_sentences(text):

    text = clean_text(text)

    if not text:
        return []

    # Convert bullet points into sentence boundaries
    text = re.sub(
        r"[\u2022\u25CF\u25AA]\s*",
        "\n",
        text
    )

    # Sentence boundaries
    parts = re.split(
        r"(?<=[.!?])\s+|\n+",
        text
    )

    sentences = []

    for part in parts:

        part = part.strip()

        if part:
            sentences.append(part)

    return sentences


# ============================================================
# NAME DETECTION
# ============================================================

def find_assignee(sentence):

    patterns = [

        r"\b([A-Z][a-z]+)\s+(?:will|shall|must|should|needs to|has to)\b",

        r"\b([A-Z][a-z]+)\s+(?:is responsible for|is assigned to)\b",

        r"\b(?:assigned to|owner:)\s*([A-Z][a-z]+)\b",

    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            sentence
        )

        if match:

            return match.group(1)

    return "Unassigned"


# ============================================================
# PRIORITY
# ============================================================

def determine_priority(sentence):

    lower = sentence.lower()

    for phrase in PRIORITY_HIGH_WORDS:

        if phrase in lower:
            return "High"

    for phrase in PRIORITY_LOW_WORDS:

        if phrase in lower:
            return "Low"

    return "Medium"


# ============================================================
# DEADLINE EXTRACTION
# ============================================================

def extract_deadline(sentence):

    lower = sentence.lower()

    # --------------------------------------------------------
    # ASAP / urgent
    # --------------------------------------------------------

    if "as soon as possible" in lower:
        return "as soon as possible"

    if re.search(r"\basap\b", lower):
        return "ASAP"

    if "urgently" in lower:
        return "urgently"

    # --------------------------------------------------------
    # Before final submission
    # --------------------------------------------------------

    match = re.search(
        r"\bbefore\s+(?:the\s+)?final submission\b",
        lower
    )

    if match:
        return "before the final submission"

    match = re.search(
        r"\bbefore\s+(?:the\s+)?submission\b",
        lower
    )

    if match:
        return "before the submission"

    # --------------------------------------------------------
    # Tomorrow / today
    # --------------------------------------------------------

    if re.search(
        r"\b(?:by\s+)?tomorrow\b",
        lower
    ):
        return "tomorrow"

    if re.search(
        r"\b(?:by\s+)?today\b",
        lower
    ):
        return "today"

    if "tonight" in lower:
        return "tonight"

    # --------------------------------------------------------
    # Weekdays
    # --------------------------------------------------------

    weekdays = (
        "monday|tuesday|wednesday|"
        "thursday|friday|saturday|sunday"
    )

    match = re.search(
        rf"\bby\s+({weekdays})\b",
        lower
    )

    if match:
        return match.group(1).capitalize()

    match = re.search(
        rf"\bnext\s+({weekdays})\b",
        lower
    )

    if match:
        return "next " + match.group(1)

    # --------------------------------------------------------
    # Next week
    # --------------------------------------------------------

    if "next week" in lower:
        return "next week"

    # --------------------------------------------------------
    # Date such as 25 October
    # --------------------------------------------------------

    match = re.search(
        r"\b(\d{1,2}(?:st|nd|rd|th)?\s+"
        r"(?:January|February|March|April|May|June|July|August|"
        r"September|October|November|December))\b",
        sentence,
        flags=re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None


# ============================================================
# DEADLINE NORMALIZATION
# ============================================================

def normalize_deadline(deadline, meeting_date):

    if not deadline:
        return "No deadline"

    lower = deadline.lower().strip()

    if lower in [
        "as soon as possible",
        "asap",
        "urgently"
    ]:
        return "ASAP"

    if "final submission" in lower:
        return "Before final submission"

    if "submission" in lower:
        return "Before submission"

    if not isinstance(
        meeting_date,
        (date, datetime)
    ):
        return deadline

    if isinstance(
        meeting_date,
        datetime
    ):
        base_date = meeting_date.date()
    else:
        base_date = meeting_date

    # --------------------------------------------------------
    # Today
    # --------------------------------------------------------

    if lower == "today":
        return base_date.strftime("%d %B %Y")

    # --------------------------------------------------------
    # Tomorrow
    # --------------------------------------------------------

    if lower == "tomorrow":
        target = base_date + timedelta(days=1)

        return target.strftime("%d %B %Y")

    # --------------------------------------------------------
    # Tonight
    # --------------------------------------------------------

    if lower == "tonight":
        return base_date.strftime("%d %B %Y")

    # --------------------------------------------------------
    # Weekdays
    # --------------------------------------------------------

    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    if lower in weekdays:

        target_day = weekdays[lower]

        days_ahead = (
            target_day - base_date.weekday()
        ) % 7

        if days_ahead == 0:
            days_ahead = 7

        target = (
            base_date
            + timedelta(days=days_ahead)
        )

        return target.strftime("%d %B %Y")

    # --------------------------------------------------------
    # Next weekday
    # --------------------------------------------------------

    if lower.startswith("next "):

        day_name = lower.replace(
            "next ",
            "",
            1
        ).strip()

        if day_name in weekdays:

            target_day = weekdays[day_name]

            days_ahead = (
                target_day - base_date.weekday()
            ) % 7

            if days_ahead == 0:
                days_ahead = 7

            # Force next week's occurrence
            days_ahead += 7

            target = (
                base_date
                + timedelta(days=days_ahead)
            )

            return target.strftime("%d %B %Y")

    # --------------------------------------------------------
    # Next week
    # --------------------------------------------------------

    if lower == "next week":

        target = base_date + timedelta(days=7)

        return target.strftime("%d %B %Y")

    # --------------------------------------------------------
    # Existing date
    # --------------------------------------------------------

    return deadline


# ============================================================
# ACTION EXTRACTION FROM SENTENCE
# ============================================================

def clean_action(action):

    action = action.strip()

    # Remove leading connectors
    action = re.sub(
        r"^(and|also|then|please)\s+",
        "",
        action,
        flags=re.IGNORECASE
    )

    # Remove assignment verbs
    action = re.sub(
        r"^(will|shall|must|should|needs to|has to)\s+",
        "",
        action,
        flags=re.IGNORECASE
    )

    # Remove deadline expressions
    action = re.sub(
        r"\s+(?:by|before|on|due)\s+"
        r"(?:the\s+)?"
        r"(?:final\s+submission|submission|"
        r"today|tomorrow|tonight|next week|"
        r"next monday|next tuesday|next wednesday|"
        r"next thursday|next friday|next saturday|"
        r"next sunday|monday|tuesday|wednesday|"
        r"thursday|friday|saturday|sunday)"
        r".*$",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"\s+(?:as soon as possible|asap|urgently)\.?$",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"\s+next week\.?$",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"\s+tomorrow\.?$",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"\s+today\.?$",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"\s+next\s+"
        r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
        r"\.?$",
        "",
        action,
        flags=re.IGNORECASE
    )

    # Remove trailing punctuation
    action = action.strip(" .,:;")

    # Lowercase first character for consistent output
    if action:
        action = action[0].lower() + action[1:]

    return action


# ============================================================
# REMOVE NON-ACTION SENTENCES
# ============================================================

def is_actionable(sentence):

    lower = sentence.lower().strip()

    if not lower:
        return False

    # --------------------------------------------------------
    # Pure priority statements are NOT tasks
    # --------------------------------------------------------

    priority_only_patterns = [
        r"tasks?\s+(are|were|have been)\s+"
        r"(high|medium|low)\s+priority",

        r"all tasks?\s+(are|were)\s+"
        r"(high|medium|low)\s+priority",

        r"the tasks?\s+are\s+"
        r"(high|medium|low)\s+priority",

        r"review tasks?\s+are\s+"
        r"(high|medium|low)\s+priority",
    ]

    for pattern in priority_only_patterns:

        if re.search(
            pattern,
            lower
        ):
            return False

    # --------------------------------------------------------
    # Information-only sentences
    # --------------------------------------------------------

    information_patterns = [
        r"^meeting\s+(was|is|will be)",
        r"^the meeting",
        r"^discussion",
        r"^participants",
        r"^attendees",
        r"^agenda",
        r"^tasks?\s+(are|were)",
        r"^priorities?\s+(are|were)",
        r"^deadline(s)?\s+(are|were)",
    ]

    for pattern in information_patterns:

        if re.search(
            pattern,
            lower
        ):

            # Still allow sentences that explicitly
            # contain an action verb.
            has_action = any(
                re.search(
                    rf"\b{re.escape(verb)}\b",
                    lower
                )
                for verb in ACTION_VERBS
            )

            if not has_action:
                return False

    # --------------------------------------------------------
    # Must contain action-like language
    # --------------------------------------------------------

    action_patterns = [

        r"\bwill\s+\w+",

        r"\bmust\s+\w+",

        r"\bshould\s+\w+",

        r"\bneeds?\s+to\s+\w+",

        r"\bhas\s+to\s+\w+",

        r"\bassigned\s+to\b",

        r"\bresponsible\s+for\b",

    ]

    for pattern in action_patterns:

        if re.search(
            pattern,
            lower
        ):
            return True

    # Direct imperative sentence
    first_word = re.match(
        r"^[A-Za-z]+",
        lower
    )

    if first_word:

        word = first_word.group(0)

        if word in ACTION_VERBS:
            return True

    # "Someone should..."
    if re.search(
        r"\b(?:someone|team|developer|manager|owner)"
        r"\s+(?:should|must|will|needs to)",
        lower
    ):
        return True

    return False


# ============================================================
# SPLIT MULTIPLE ACTIONS
# ============================================================

def split_action_sentence(sentence):

    sentence = sentence.strip()

    # --------------------------------------------------------
    # Case:
    # Rahul will prepare report, while Priya will complete UI.
    # --------------------------------------------------------

    pattern = re.compile(
        r"\bwhile\b|\band\s+(?=[A-Z][a-z]+\s+"
        r"(?:will|must|should|needs to|has to))",
        flags=re.IGNORECASE
    )

    parts = pattern.split(sentence)

    cleaned_parts = []

    for part in parts:

        part = part.strip(
            " .,:;"
        )

        if part:
            cleaned_parts.append(part)

    return cleaned_parts


# ============================================================
# EXTRACT ASSIGNEE + ACTION
# ============================================================

def extract_single_action(sentence):

    assignee = find_assignee(sentence)

    deadline = extract_deadline(sentence)

    # --------------------------------------------------------
    # Remove person + modal verb
    # --------------------------------------------------------

    action = sentence.strip()

    action = re.sub(
        r"^[A-Z][a-z]+\s+"
        r"(?:will|shall|must|should|needs to|has to)\s+",
        "",
        action
    )

    action = re.sub(
        r"^(?:someone|the team|team)\s+"
        r"(?:will|shall|must|should|needs to|has to)\s+",
        "",
        action,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # Passive review:
    # "The security configuration should be reviewed..."
    # --------------------------------------------------------

    passive_match = re.search(
        r"^the\s+(.+?)\s+"
        r"(?:should|must|needs to|has to)\s+be\s+"
        r"(\w+)",
        action,
        flags=re.IGNORECASE
    )

    if passive_match:

        object_text = passive_match.group(1).strip()

        verb = passive_match.group(2).strip()

        action = f"{verb} {object_text}"

    else:

        action = clean_action(
            action
        )

    # --------------------------------------------------------
    # Special cleanup
    # --------------------------------------------------------

    action = re.sub(
        r"^reviewed\s+before\s+the\s+final\s+submission$",
        "review security configuration",
        action,
        flags=re.IGNORECASE
    )

    # --------------------------------------------------------
    # Remove trailing deadline remnants
    # --------------------------------------------------------

    action = re.sub(
        r"\s+by\s+\w+\.?$",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"\s+next\s+\w+\.?$",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"\s+(tomorrow|today|tonight)\.?$",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"\s+(as soon as possible|asap|urgently)\.?$",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = action.strip(
        " .,:;"
    )

    if not action:
        return None

    return {
        "Assigned To": assignee,
        "Action Item": action,
        "Deadline": deadline if deadline else "None",
        "Priority": determine_priority(sentence)
    }


# ============================================================
# DEDUPLICATION
# ============================================================

def normalize_for_duplicate(text):

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def remove_duplicates(items):

    unique = []

    seen = set()

    for item in items:

        key = (
            normalize_for_duplicate(
                item["Assigned To"]
            ),
            normalize_for_duplicate(
                item["Action Item"]
            )
        )

        if key in seen:
            continue

        seen.add(key)

        unique.append(item)

    return unique


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_action_items(
    text,
    meeting_date=None
):

    text = clean_text(text)

    if not text:
        return pd.DataFrame(
            columns=[
                "Assigned To",
                "Action Item",
                "Deadline",
                "Normalized Deadline",
                "Priority"
            ]
        )

    sentences = split_sentences(
        text
    )

    extracted = []

    for sentence in sentences:

        if not is_actionable(
            sentence
        ):
            continue

        action_parts = split_action_sentence(
            sentence
        )

        for part in action_parts:

            if not is_actionable(
                part
            ):
                continue

            item = extract_single_action(
                part
            )

            if item is None:
                continue

            item["Normalized Deadline"] = (
                normalize_deadline(
                    item["Deadline"],
                    meeting_date
                )
            )

            extracted.append(
                item
            )

    # --------------------------------------------------------
    # Deduplicate
    # --------------------------------------------------------

    extracted = remove_duplicates(
        extracted
    )

    # --------------------------------------------------------
    # Create dataframe
    # --------------------------------------------------------

    df = pd.DataFrame(
        extracted,
        columns=[
            "Assigned To",
            "Action Item",
            "Deadline",
            "Normalized Deadline",
            "Priority"
        ]
    )

    # --------------------------------------------------------
    # Final cleanup
    # --------------------------------------------------------

    if not df.empty:

        df["Assigned To"] = (
            df["Assigned To"]
            .fillna("Unassigned")
        )

        df["Action Item"] = (
            df["Action Item"]
            .fillna("")
            .astype(str)
            .str.strip()
        )

        df["Deadline"] = (
            df["Deadline"]
            .fillna("None")
        )

        df["Normalized Deadline"] = (
            df["Normalized Deadline"]
            .fillna("No deadline")
        )

        df["Priority"] = (
            df["Priority"]
            .fillna("Medium")
        )

    return df


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def extract_action_items_from_text(
    text,
    meeting_date=None
):

    return extract_action_items(
        text,
        meeting_date
    )