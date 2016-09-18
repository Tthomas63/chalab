class s():
    Str = lambda: None
    Optional = lambda x: None
    Bool = lambda: None
    Date = lambda: None
    Int = lambda: None


class Field:
    pass


class Str(Field):
    pass


class Optional(Field):
    def __init__(self, content):
        self._content = content


class Bool(Field):
    pass


class Date(Field):
    pass


class Int(Field):
    pass


DocumentationSchema = {
    "overview": Str(),
    "evaluation": Str(),
    "terms": Str(),
    "data": Str(),
    Str(): Str(),
}

CompetitionSchema = {
    "title": Str(),
    "image": Str(),
    "has_registration": Bool(),
    Optional("end_date"): Date(),
    "html": DocumentationSchema,

    "phases": {
        Int(): {
            "phasenumber": Int(),
            "label": Str(),
            "description": Str(),
            Optional("max_submissions"): Int(),
            Optional("max_submissions_per_day"): Int(),
            "scoring_program": Str(),
            "reference_data": Str()
        }
    },

    "leaderboard": {
        "leaderboards": {
        },
        "columns": {
        }
    }
}
