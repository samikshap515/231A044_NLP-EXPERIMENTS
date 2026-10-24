import re
import calendar
import pandas as pd

from datetime import date, datetime, timedelta


# ============================================================
# MONTHS AND WEEKDAYS
# ============================================================

MONTHS = {
    name.lower(): number
    for number, name in enumerate(calendar.month_name)
    if name
}

WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6
}


# ============================================================
# WORD LISTS
# ============================================================

ACTION_VERBS = {
    "prepare",
    "review",
    "update",
    "create",
    "send",
    "schedule",
    "test",
    "finalize",
    "develop",
    "analyze",
    "check",
    "organize",
    "arrange",
    "fix",
    "implement",
    "design",
    "deploy",
    "write",
    "edit",
    "verify",
    "validate",
    "configure",
    "install",
    "build",
    "document",
    "present",
    "research",
    "collect",
    "compile",
    "call",
    "contact",
    "email",
    "upload",
    "download",
    "generate",
    "assign",
    "coordinate",
    "communicate",
    "investigate",
    "manage",
    "conduct",
    "perform",
    "monitor",
    "handle",
    "deliver",
    "produce",
    "establish",
    "distribute",
    "confirm",
    "approve",
    "resolve",
    "address",
    "follow",
    "submit",
    "start",
    "complete",
    "escalate",
    "inform",
    "notify",
    "meet",
    "ensure",
    "plan",
    "improve",
    "remove",
    "add",
    "change",
    "support",
    "maintain",
    "track",
    "troubleshoot",
    "summarize",
    "audit",
    "review",
    "prepare",
    "decide",
    "continue",
    "require",
    "investigate"
}


STOP_WORDS = {
    "the",
    "a",
    "an",
    "this",
    "that",
    "these",
    "those",
    "we",
    "you",
    "i",
    "he",
    "she",
    "they",
    "it",
    "someone",
    "somebody",
    "anyone",
    "anybody",
    "everyone",
    "everybody",
    "person",
    "people",
    "team",
    "staff",
    "manager",
    "employee",
    "member",
    "assigned",
    "unassigned",
    "none",
    "no",
    "whether",
    "what",
    "which",
    "where",
    "when",
    "why",
    "how",
    "will",
    "shall",
    "should",
    "must",
    "can",
    "could",
    "would",
    "may",
    "might",
    "need",
    "needs",
    "needed",
    "please",
    "responsible",
    "tasked",
    "required",
    "expected",
    "agreed",
    "today",
    "tomorrow",
    "tonight",
    "asap",
    "urgently",
    "immediately",
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday"
}


INVALID_ACTION_WORDS = {
    "be",
    "is",
    "are",
    "was",
    "were",
    "been",
    "being",
    "has",
    "have",
    "had",
    "discuss",
    "discussed",
    "discussing",
    "talk",
    "talked",
    "talking",
    "mention",
    "mentioned",
    "mentioning",
    "finish",
    "finished",
    "complete",
    "completed",
    "submit",
    "submitted"
}


URGENCY_PHRASES = {
    "as soon as possible",
    "asap",
    "right away",
    "without delay",
    "immediately",
    "urgent",
    "urgently",
    "critical",
    "high priority",
    "top priority",
    "highest priority",
    "needs immediate attention",
    "immediate attention",
    "time sensitive",
    "time-sensitive"
}


HIGH_WORDS = {
    "urgent",
    "urgently",
    "immediately",
    "asap",
    "critical",
    "emergency",
    "important",
    "security",
    "breach",
    "incident",
    "outage",
    "production",
    "blocked",
    "blocker",
    "must",
    "escalate",
    "escalation"
}


LOW_WORDS = {
    "optional",
    "whenever",
    "eventually",
    "later",
    "nonurgent",
    "non-urgent",
    "nice-to-have",
    "nice to have"
}


# ============================================================
# DEADLINE PATTERN
# ============================================================

DEADLINE_REGEX = re.compile(
    r"""
    (?:
        \b(?:by|before|until|on|for|due(?:\s+on)?)\s+
        (?:the\s+)?
        (?:
            end\s+of\s+(?:this|next)\s+week
            |
            next\s+(?:week|month|
                monday|tuesday|wednesday|thursday|
                friday|saturday|sunday)
            |
            this\s+(?:week|month|
                monday|tuesday|wednesday|thursday|
                friday|saturday|sunday)
            |
            today|tomorrow|tonight|
            asap|immediately|urgently|
            as\s+soon\s+as\s+possible|
            in\s+\d+\s+(?:day|days|week|weeks|month|months)|
            in\s+(?:one|a)\s+(?:day|week|month)|
            monday|tuesday|wednesday|thursday|
            friday|saturday|sunday|
            \d{1,2}(?:st|nd|rd|th)?\s+
            (?:january|february|march|april|may|june|
             july|august|september|october|november|december)
            (?:\s+\d{4})?
        )
        |
        \bend\s+of\s+(?:this|next)\s+week\b
        |
        \bnext\s+(?:week|month|
            monday|tuesday|wednesday|thursday|
            friday|saturday|sunday)\b
        |
        \bthis\s+(?:week|month|
            monday|tuesday|wednesday|thursday|
            friday|saturday|sunday)\b
        |
        \b(?:today|tomorrow|tonight|asap)\b
        |
        \b(?:immediately|urgently)\b
        |
        \bas\s+soon\s+as\s+possible\b
        |
        \bin\s+\d+\s+(?:day|days|week|weeks|month|months)\b
        |
        \bin\s+(?:one|a)\s+(?:day|week|month)\b
        |
        \b(?:monday|tuesday|wednesday|thursday|
            friday|saturday|sunday)\b
        |
        \b\d{1,2}(?:st|nd|rd|th)?\s+
        (?:january|february|march|april|may|june|
         july|august|september|october|november|december)
        (?:\s+\d{4})?
    )
    """,
    re.IGNORECASE | re.VERBOSE
)


# ============================================================
# BASIC HELPERS
# ============================================================

def empty_result():
    return pd.DataFrame(
        columns=[
            "Assigned To",
            "Action Item",
            "Deadline",
            "Normalized Deadline",
            "Priority"
        ]
    )


def clean_text(text):
    if text is None:
        return ""

    text = re.sub(r"\s+", " ", str(text))
    return text.strip(" ,.;:!?-")


def normalize_person_name(name):
    if not name:
        return None

    name = clean_text(name)

    name = re.sub(
        r"^(?:the|a|an)\s+",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = name.strip(" ,.;:!?-")

    if not name:
        return None

    if name.lower() in STOP_WORDS:
        return None

    if len(name.split()) > 3:
        return None

    if not re.fullmatch(
        r"[A-Za-z]+(?:[-'][A-Za-z]+)?(?:\s+[A-Za-z]+(?:[-'][A-Za-z]+)?){0,2}",
        name
    ):
        return None

    words = name.split()

    if any(word.lower() in STOP_WORDS for word in words):
        return None

    return " ".join(
        word.capitalize()
        for word in words
    )


def is_valid_person(name):
    return normalize_person_name(name) is not None


def remove_deadline_from_sentence(sentence, deadline_span):
    if not deadline_span:
        return sentence.strip()

    start, end = deadline_span

    result = (
        sentence[:start] +
        " " +
        sentence[end:]
    )

    return clean_text(result)


# ============================================================
# SENTENCE SPLITTING
# ============================================================

def split_meeting_sentences(text):
    text = str(text or "").replace("\r", "\n").strip()

    if not text:
        return []

    sentences = []

    for line in text.split("\n"):
        line = clean_text(line)

        if not line:
            continue

        parts = re.split(
            r"(?<=[.!?])\s+(?=[A-Z])",
            line
        )

        for part in parts:
            part = clean_text(part)

            if part:
                sentences.append(part)

    return sentences


# ============================================================
# DEADLINE EXTRACTION
# ============================================================

def strip_deadline_prefix(text):
    text = clean_text(text)

    return re.sub(
        r"^(?:by|before|until|on|for|due(?:\s+on)?)\s+",
        "",
        text,
        flags=re.IGNORECASE
    ).strip()


def extract_deadline(sentence):
    matches = list(
        DEADLINE_REGEX.finditer(sentence)
    )

    if not matches:
        return None, None

    match = matches[-1]

    raw_deadline = clean_text(
        match.group(0)
    )

    deadline = strip_deadline_prefix(
        raw_deadline
    )

    return deadline, match.span()


# ============================================================
# PERSON EXTRACTION
# ============================================================

def extract_person(sentence):
    """
    Detects people only from safe assignment patterns.

    Examples handled:

    Rahul will prepare the report.
    Priya should review the document.
    The report needs to be prepared by Rahul.
    The document should be reviewed by Priya.
    Please make sure Neha handles the project report.
    Rahul is responsible for preparing the final report.
    Priya has been asked to update the spreadsheet.
    The task is assigned to Rohan.
    """

    text = clean_text(sentence)

    patterns = [

        # Rahul will prepare...
        # Rahul should review...
        # Rahul must complete...
        r"^\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\s+"
        r"(?:will|shall|should|must|can|could|would|may|might)\b",

        # Please make sure Neha handles...
        r"\bmake\s+sure\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\s+"
        r"(?:handles?|prepares?|reviews?|updates?|completes?|"
        r"investigates?|arranges?|coordinates?|manages?|"
        r"checks?|audits?|creates?|writes?|sends?)\b",

        # Neha is responsible for...
        r"^\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\s+"
        r"is\s+responsible\s+for\b",

        # Priya has been asked to...
        r"^\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\s+"
        r"has\s+been\s+asked\s+to\b",

        # The report needs to be prepared by Rahul.
        r"\bprepared\s+by\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b",

        # The document should be reviewed by Priya.
        r"\breviewed\s+by\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b",

        # The presentation must be completed by Amit.
        r"\bcompleted\s+by\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b",

        # The task is assigned to Rohan.
        r"\bassigned\s+to\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b",

        # General "by Rahul" fallback.
        r"\bby\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b",

        # General "for Rahul" fallback.
        r"\bfor\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})\b"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text
        )

        if not match:
            continue

        possible_name = match.group(1)

        person = normalize_person_name(
            possible_name
        )

        if person:
            return person

    # Additional patterns for "Someone should..." and "The team should..."
    # Someone should investigate...
    someone_match = re.search(r"([A-Z][a-z]+)\s+should\s+(?:investigates?|researches?)", text)
    if someone_match:
        person = normalize_person_name(someone_match.group(1))
        if person:
            return person
    # The team should check...
    team_match = re.search(r"the\s+team\s+should\s+(?:checks?|reviews?)", text)
    if team_match:
        # No specific person, return Unassigned
        return "Unassigned"

    return None


# ============================================================
# ACTION EXTRACTION
# ============================================================

def normalize_action(action):
    if not action:
        return ""

    action = clean_text(action)

    action = re.sub(
        r"^(?:please\s+)?",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"^(?:you\s+)?",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"^(?:to\s+)",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"^(?:be\s+)",
        "",
        action,
        flags=re.IGNORECASE
    )

    action = re.sub(
        r"\s+",
        " ",
        action
    )

    action = action.strip(
        " ,.;:!?-"
    )

    if not action:
        return ""

    return action.lower()


def find_first_action_word(text):
    words = re.findall(
        r"[A-Za-z]+(?:'[A-Za-z]+)?",
        text.lower()
    )

    for index, word in enumerate(words):
        if word in ACTION_VERBS:
            return index, word

    return None, None


def extract_action(sentence, deadline_span=None):
    text_without_deadline = remove_deadline_from_sentence(
        sentence,
        deadline_span
    )

    text = clean_text(
        text_without_deadline
    )

    # --------------------------------------------------------
    # Pattern 1:
    # Rahul will investigate the security issue
    # Priya should coordinate with the client
    # --------------------------------------------------------

    match = re.search(
        r"\b(?:will|shall|should|must|can|could|would|may|might)\s+"
        r"(.+)$",
        text,
        flags=re.IGNORECASE
    )

    if match:
        action = normalize_action(
            match.group(1)
        )

        action = re.sub(
            r"^(?:be\s+)",
            "",
            action,
            flags=re.IGNORECASE
        )

        if action:
            return action

    # --------------------------------------------------------
    # Pattern 2:
    # Rahul is responsible for preparing the report
    # --------------------------------------------------------

    match = re.search(
        r"\bis\s+responsible\s+for\s+(.+)$",
        text,
        flags=re.IGNORECASE
    )

    if match:
        return normalize_action(
            match.group(1)
        )

    # --------------------------------------------------------
    # Pattern 3:
    # Priya has been asked to update the spreadsheet
    # --------------------------------------------------------

    match = re.search(
        r"\bhas\s+been\s+asked\s+to\s+(.+)$",
        text,
        flags=re.IGNORECASE
    )

    if match:
        return normalize_action(
            match.group(1)
        )

    # --------------------------------------------------------
    # Pattern 4:
    # Please make sure Neha handles the project report
    # --------------------------------------------------------

    match = re.search(
        r"\bmake\s+sure\s+"
        r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\s+"
        r"(.+)$",
        text
    )

    if match:
        action = normalize_action(
            match.group(1)
        )

        return action

    # --------------------------------------------------------
    # Pattern 5:
    # The report needs to be prepared by Rahul
    # The document should be reviewed by Priya
    # --------------------------------------------------------

    passive_patterns = [
        r"\bneeds?\s+to\s+be\s+(.+?)(?:\s+by\s+[A-Z][a-z]+.*)?$",
        r"\bshould\s+be\s+(.+?)(?:\s+by\s+[A-Z][a-z]+.*)?$",
        r"\bmust\s+be\s+(.+?)(?:\s+by\s+[A-Z][a-z]+.*)?$",
        r"\bhas\s+to\s+be\s+(.+?)(?:\s+by\s+[A-Z][a-z]+.*)?$"
    ]

    for pattern in passive_patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:
            action = normalize_action(
                match.group(1)
            )

            return action

    # --------------------------------------------------------
    # Pattern 6:
    # The task is assigned to Rohan
    # --------------------------------------------------------

    match = re.search(
        r"^\s*the\s+(.+?)\s+is\s+assigned\s+to\s+",
        text,
        flags=re.IGNORECASE
    )

    if match:
        task_name = normalize_action(
            match.group(1)
        )

        if task_name:
            return "assign " + task_name

    # --------------------------------------------------------
    # Pattern 7:
    # Generic fallback using action verbs
    # --------------------------------------------------------

    action_index, action_word = find_first_action_word(
        text
    )

    if action_index is not None:
        words = text.split()

        selected_words = []

        found_action = False

        for word in words:
            clean_word = re.sub(
                r"[^A-Za-z'-]",
                "",
                word
            ).lower()

            if not found_action:
                if clean_word in ACTION_VERBS:
                    found_action = True
                    selected_words.append(
                        clean_word
                    )
            else:
                selected_words.append(
                    word
                )

        if selected_words:
            return normalize_action(
                " ".join(selected_words)
            )

    return ""


# ============================================================
# ACTION SENTENCE DETECTION
# ============================================================

def is_discussion_statement(sentence):
    text = sentence.lower()

    discussion_patterns = [
        r"\bdiscussed\b",
        r"\bdiscussing\b",
        r"\btalked\s+about\b",
        r"\btalking\s+about\b",
        r"\bmentioned\b",
        r"\bwas\s+discussed\b",
        r"\bwere\s+discussed\b"
    ]

    return any(
        re.search(
            pattern,
            text
        )
        for pattern in discussion_patterns
    )


def is_completed_statement(sentence):
    text = sentence.lower()

    completed_patterns = [
        r"\bwas\s+completed\b",
        r"\bwere\s+completed\b",
        r"\bhas\s+been\s+completed\b",
        r"\bhave\s+been\s+completed\b",
        r"\bwas\s+finished\b",
        r"\bwere\s+finished\b",
        r"\bhas\s+been\s+finished\b",
        r"\bhave\s+been\s+finished\b",
        r"\bwas\s+submitted\b",
        r"\bwere\s+submitted\b",
        r"\bhas\s+been\s+submitted\b",
        r"\bhave\s+been\s+submitted\b"
    ]

    return any(
        re.search(
            pattern,
            text
        )
        for pattern in completed_patterns
    )


def is_action_sentence(sentence):
    if is_discussion_statement(sentence):
        return False

    if is_completed_statement(sentence):
        return False

    deadline, _ = extract_deadline(
        sentence
    )

    action = extract_action(
        sentence
    )

    if action:
        return True

    if deadline:
        return True

    return False


# ============================================================
# DEADLINE NORMALIZATION
# ============================================================

def normalize_deadline(deadline_text, meeting_date):
    if not deadline_text:
        return None

    if isinstance(meeting_date, datetime):
        meeting_date = meeting_date.date()

    if not isinstance(meeting_date, date):
        meeting_date = date.today()

    # Handle "by [weekday]" BEFORE strip_deadline_prefix removes "by"
    # e.g., "by Monday" -> next Monday, not this week's Monday
    original_text = deadline_text.lower().strip()
    by_match = re.match(r'^by\s+', original_text)
    if by_match:
        plain_day = original_text[3:].strip()
        if plain_day in WEEKDAYS:
            target_weekday = WEEKDAYS[plain_day]
            days_ahead = (
                target_weekday -
                meeting_date.weekday()
            ) % 7
            # If days_ahead is 0, the meeting is on that day, so go to next week
            if days_ahead <= 0:
                days_ahead += 7
            return meeting_date + timedelta(days=days_ahead)

    # Handle event-based deadlines: "before [event]" BEFORE strip_deadline_prefix removes "before"
    # e.g., "before the final submission" should be preserved as event-based
    original_text = deadline_text.lower().strip()
    if original_text.startswith("before "):
        event_part = original_text[7:].strip()  # text after "before "
        event_indicators = {
            "submission",
            "final",
            "review",
            "check",
            "audit",
            "performance",
            "meeting",
            "deadline",
            "configuration",
            "report"
        }
        if any(ind in event_part.lower() for ind in event_indicators):
            return "Event-based: " + deadline_text

    text = strip_deadline_prefix(
        deadline_text
    ).lower().strip()
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    # ASAP / URGENT
    if text in {
        "asap",
        "immediately",
        "urgently",
        "as soon as possible"
    }:
        return "ASAP"

    # TODAY
    if text == "today":
        return meeting_date

    # TOMORROW
    if text == "tomorrow":
        return meeting_date + timedelta(
            days=1
        )

    # TONIGHT
    if text == "tonight":
        return meeting_date

    # NEXT WEEK
    if text == "next week":
        return meeting_date + timedelta(
            days=7
        )    # PLAIN WEEKDAY - just the day name, treated as the next occurrence
    if text in WEEKDAYS:
        target_weekday = WEEKDAYS[text]

        days_ahead = (
            target_weekday -
            meeting_date.weekday()
        ) % 7

        # If days_ahead is 0, the meeting is on that day, so go to next week
        if days_ahead == 0:
            days_ahead = 7

        return meeting_date + timedelta(days=days_ahead)

    # Handle "by [weekday]" - by Monday means next Monday, not this week's Monday
    # Strip "by" prefix and re-check as plain weekday
    by_match = re.match(r'^by\s+', text)
    if by_match:
        plain_day = text[3:].strip()
        if plain_day in WEEKDAYS:
            target_weekday = WEEKDAYS[plain_day]
            days_ahead = (
                target_weekday -
                meeting_date.weekday()
            ) % 7
            # If days_ahead is 0, the meeting is on that day, so go to next week
            if days_ahead <= 0:
                days_ahead += 7
            return meeting_date + timedelta(days=days_ahead)

    # THIS WEEK
    if text == "this week":
        monday = meeting_date - timedelta(
            days=meeting_date.weekday()
        )

        return monday + timedelta(days=4)

    # NEXT MONTH
    if text == "next month":
        if meeting_date.month == 12:
            return date(
                meeting_date.year + 1,
                1,
                1
            )

        return date(
            meeting_date.year,
            meeting_date.month + 1,
            1
        )

    # THIS MONTH
    if text == "this month":
        if meeting_date.month == 12:
            next_month = date(
                meeting_date.year + 1,
                1,
                1
            )
        else:
            next_month = date(
                meeting_date.year,
                meeting_date.month + 1,
                1
            )

        return next_month - timedelta(
            days=1
        )

    # IN N DAYS / WEEKS / MONTHS
    match = re.fullmatch(
        r"in\s+(\d+|one|a)\s+"
        r"(day|days|week|weeks|month|months)",
        text
    )

    if match:
        number_text, unit = match.groups()

        number = (
            1
            if number_text in {"one", "a"}
            else int(number_text)
        )

        if unit.startswith("day"):
            return meeting_date + timedelta(
                days=number
            )

        if unit.startswith("week"):
            return meeting_date + timedelta(
                days=7 * number
            )

        if unit.startswith("month"):
            return meeting_date + timedelta(
                days=30 * number
            )

    # NEXT WEEKDAY
    match = re.fullmatch(
        r"next\s+"
        r"(monday|tuesday|wednesday|thursday|"
        r"friday|saturday|sunday)",
        text
    )

    if match:
        target_weekday = WEEKDAYS[
            match.group(1)
        ]

        days_ahead = (
            target_weekday -
            meeting_date.weekday()
        ) % 7

        if days_ahead == 0:
            days_ahead = 7

        return (
            meeting_date +
            timedelta(days=days_ahead)
        )

    # THIS WEEKDAY
    match = re.fullmatch(
        r"this\s+"
        r"(monday|tuesday|wednesday|thursday|"
        r"friday|saturday|sunday)",
        text
    )

    if match:
        target_weekday = WEEKDAYS[
            match.group(1)
        ]

        monday = meeting_date - timedelta(
            days=meeting_date.weekday()
        )

        result = monday + timedelta(
            days=target_weekday
        )

        if result < meeting_date:
            result += timedelta(
                days=7
            )

        return result

    # PLAIN WEEKDAY
    if text in WEEKDAYS:
        target_weekday = WEEKDAYS[
            text
        ]

        days_ahead = (
            target_weekday -
            meeting_date.weekday()
        ) % 7

        return meeting_date + timedelta(
            days=days_ahead
        )

    # ABSOLUTE DATE - no auto year increment
    # If year not specified, just use the current year
    match = re.fullmatch(
        r"(\d{1,2})(?:st|nd|rd|th)?\s+"
        r"([a-z]+)"
        r"(?:\s+(\d{4}))?",
        text
    )

    if match:
        day = int(
            match.group(1)
        )

        month = MONTHS.get(
            match.group(2).lower()
        )

        year = (
            int(match.group(3))
            if match.group(3)
            else meeting_date.year
        )

        if month:
            try:
                return date(year, month, day)

            except ValueError:
                return None

    return None


def format_normalized(value):
    if isinstance(value, date):
        return value.strftime(
            "%d %B %Y"
        )

    if value:
        return str(value)

    return "No deadline"


# ============================================================
# PRIORITY DETECTION
# ============================================================

def detect_priority(
    action,
    sentence,
    deadline_text,
    normalized_date,
    meeting_date
):
    combined_text = (
        f"{sentence} {action}"
    ).lower()

    high_score = 0
    low_score = 0

    for phrase in URGENCY_PHRASES:
        if phrase in combined_text:
            high_score += 4

    for word in HIGH_WORDS:
        if re.search(
            rf"\b{re.escape(word)}\b",
            combined_text
        ):
            high_score += 2

    for phrase in LOW_WORDS:
        if phrase in combined_text:
            low_score += 2

    if deadline_text:
        deadline_lower = deadline_text.lower()

        if any(
            phrase in deadline_lower
            for phrase in {
                "asap",
                "immediately",
                "urgently",
                "as soon as possible"
            }
        ):
            high_score += 5

        elif any(
            word in deadline_lower
            for word in {
                "today",
                "tomorrow",
                "tonight"
            }
        ):
            high_score += 3

        elif isinstance(
            normalized_date,
            date
        ):
            days_difference = (
                normalized_date -
                meeting_date
            ).days

            if days_difference <= 2:
                high_score += 3

            elif days_difference <= 7:
                high_score += 1

            elif days_difference >= 30:
                low_score += 2

    if (
        high_score > low_score
        and high_score >= 3
    ):
        return "High"

    if (
        low_score > high_score
        and low_score >= 2
    ):
        return "Low"

    return "Medium"


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_action_items(
    meeting_text,
    meeting_date=None
):
    if meeting_date is None:
        meeting_date = date.today()

    if isinstance(meeting_date, datetime):
        meeting_date = meeting_date.date()

    if not meeting_text or not str(
        meeting_text
    ).strip():
        return empty_result()

    rows = []

    seen = set()

    sentences = split_meeting_sentences(
        meeting_text
    )

    for sentence in sentences:
        sentence = clean_text(
            sentence
        )

        if not sentence:
            continue

        if not is_action_sentence(
            sentence
        ):
            continue

        deadline, deadline_span = extract_deadline(
            sentence
        )

        action = extract_action(
            sentence,
            deadline_span
        )

        if not action:
            continue

        if action.lower() in INVALID_ACTION_WORDS:
            continue

        person = extract_person(
            sentence
        )

        normalized_value = normalize_deadline(
            deadline,
            meeting_date
        )

        normalized_date = (
            normalized_value
            if isinstance(
                normalized_value,
                date
            )
            else None
        )

        priority = detect_priority(
            action=action,
            sentence=sentence,
            deadline_text=deadline,
            normalized_date=normalized_date,
            meeting_date=meeting_date
        )

        # Deduplication: normalize key for comparison
        person_key = "Unassigned" if person is None else person
        action_normalized = action.lower().strip()
        deadline_normalized = (normalized_value.strftime("%d %B %Y") if isinstance(normalized_value, date) else (normalized_value or "")).lower().strip()
        dedup_key = (action_normalized, deadline_normalized, person_key)

        if dedup_key in seen:
            continue  # Skip duplicate

        seen.add(dedup_key)

        rows.append(
            {
                "Assigned To": person_key,
                "Action Item": action,
                "Deadline": deadline,
                "Normalized Deadline": format_normalized(
                    normalized_value
                ),
                "Priority": priority
            }
        )

    if not rows:
        return empty_result()

    result = pd.DataFrame(
        rows,
        columns=[
            "Assigned To",
            "Action Item",
            "Deadline",
            "Normalized Deadline",
            "Priority"
        ]
    )

    return result


# ============================================================
# SUMMARY GENERATION
# ============================================================

def generate_summary(
    meeting_text,
    meeting_date=None
):
    result = extract_action_items(
        meeting_text,
        meeting_date
    )

    if result.empty:
        return (
            "No action items were identified "
            "from the meeting."
        )

    summary_parts = [
        f"{len(result)} action item(s) were identified."
    ]

    for _, row in result.iterrows():
        person = row["Assigned To"]
        action = row["Action Item"]
        deadline = row["Deadline"]
        normalized = row["Normalized Deadline"]
        priority = row["Priority"]

        if (
            pd.notna(person)
            and str(person).strip()
        ):
            summary_sentence = (
                f"{person} will {action}"
            )
        else:
            summary_sentence = (
                f"An unassigned person will {action}"
            )

        if (
            pd.notna(deadline)
            and str(deadline).strip()
            and str(deadline).lower() != "none"
        ):
            summary_sentence += (
                f" {deadline}"
            )

        if (
            pd.notna(normalized)
            and str(normalized).strip()
            and str(normalized).upper() != "NONE"
            and str(normalized).upper() != "ASAP"
        ):
            summary_sentence += (
                f" ({normalized})"
            )

        summary_sentence += (
            f" [{priority} priority]."
        )

        summary_parts.append(
            summary_sentence
        )

    return " ".join(
        summary_parts
    )