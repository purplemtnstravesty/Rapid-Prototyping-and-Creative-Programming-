# -*- coding: utf-8 -*-

import re
import os
import sys
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet

from nltk import RegexpParser
from textblob import TextBlob, Word
from textblob.sentiments import NaiveBayesAnalyzer

naive_bayes_analyzer = NaiveBayesAnalyzer()

stopwords = [
    "a",
    "a's",
    "able",
    "about",
    "above",
    "according",
    "accordingly",
    "across",
    "actually",
    "after",
    "afterwards",
    "again",
    "against",
    "ain't",
    "all",
    "allow",
    "allows",
    "almost",
    "alone",
    "along",
    "already",
    "also",
    "although",
    "always",
    "am",
    "among",
    "amongst",
    "an",
    "and",
    "another",
    "any",
    "anybody",
    "anyhow",
    "anyone",
    "anything",
    "anyway",
    "anyways",
    "anywhere",
    "apart",
    "appear",
    "appreciate",
    "appropriate",
    "are",
    "aren't",
    "around",
    "as",
    "aside",
    "ask",
    "asking",
    "associated",
    "at",
    "available",
    "away",
    "awfully",
    "b",
    "be",
    "became",
    "because",
    "become",
    "becomes",
    "becoming",
    "been",
    "before",
    "beforehand",
    "behind",
    "being",
    "believe",
    "below",
    "beside",
    "besides",
    "best",
    "better",
    "between",
    "beyond",
    "both",
    "brief",
    "but",
    "by",
    "c",
    "c'mon",
    "c's",
    "came",
    "can",
    "can't",
    "cannot",
    "cant",
    "cause",
    "causes",
    "certain",
    "certainly",
    "changes",
    "clearly",
    "co",
    "com",
    "come",
    "comes",
    "concerning",
    "consequently",
    "consider",
    "considering",
    "contain",
    "containing",
    "contains",
    "corresponding",
    "could",
    "couldn't",
    "course",
    "currently",
    "d",
    "definitely",
    "described",
    "despite",
    "did",
    "didn't",
    "different",
    "do",
    "does",
    "doesn't",
    "doing",
    "don't",
    "done",
    "down",
    "downwards",
    "during",
    "e",
    "each",
    "edu",
    "eg",
    "eight",
    "either",
    "else",
    "elsewhere",
    "enough",
    "entirely",
    "especially",
    "et",
    "etc",
    "even",
    "ever",
    "every",
    "everybody",
    "everyone",
    "everything",
    "everywhere",
    "ex",
    "exactly",
    "example",
    "except",
    "f",
    "far",
    "few",
    "fifth",
    "first",
    "five",
    "followed",
    "following",
    "follows",
    "for",
    "former",
    "formerly",
    "forth",
    "four",
    "from",
    "further",
    "furthermore",
    "g",
    "get",
    "gets",
    "getting",
    "given",
    "gives",
    "go",
    "goes",
    "going",
    "gone",
    "got",
    "gotten",
    "greetings",
    "h",
    "had",
    "hadn't",
    "happens",
    "hardly",
    "has",
    "hasn't",
    "have",
    "haven't",
    "having",
    "he",
    "he's",
    "hello",
    "help",
    "hence",
    "her",
    "here",
    "here's",
    "hereafter",
    "hereby",
    "herein",
    "hereupon",
    "hers",
    "herself",
    "hi",
    "him",
    "himself",
    "his",
    "hither",
    "hopefully",
    "how",
    "howbeit",
    "however",
    "i",
    "i'd",
    "i'll",
    "i'm",
    "i've",
    "ie",
    "if",
    "ignored",
    "immediate",
    "in",
    "inasmuch",
    "inc",
    "indeed",
    "indicate",
    "indicated",
    "indicates",
    "inner",
    "insofar",
    "instead",
    "into",
    "inward",
    "is",
    "isn't",
    "it",
    "it'd",
    "it'll",
    "it's",
    "its",
    "itself",
    "j",
    "just",
    "k",
    "keep",
    "keeps",
    "kept",
    "know",
    "knows",
    "known",
    "l",
    "last",
    "lately",
    "later",
    "latter",
    "latterly",
    "least",
    "less",
    "lest",
    "let",
    "let's",
    "like",
    "liked",
    "likely",
    "little",
    "look",
    "looking",
    "looks",
    "ltd",
    "m",
    "mainly",
    "many",
    "may",
    "maybe",
    "me",
    "mean",
    "meanwhile",
    "merely",
    "might",
    "more",
    "moreover",
    "most",
    "mostly",
    "much",
    "must",
    "my",
    "myself",
    "n",
    "name",
    "namely",
    "nd",
    "near",
    "nearly",
    "necessary",
    "need",
    "needs",
    "neither",
    "never",
    "nevertheless",
    "new",
    "next",
    "nine",
    "no",
    "nobody",
    "non",
    "none",
    "noone",
    "nor",
    "normally",
    "not",
    "nothing",
    "novel",
    "now",
    "nowhere",
    "o",
    "obviously",
    "of",
    "off",
    "often",
    "oh",
    "ok",
    "okay",
    "old",
    "on",
    "once",
    "one",
    "ones",
    "only",
    "onto",
    "or",
    "other",
    "others",
    "otherwise",
    "ought",
    "our",
    "ours",
    "ourselves",
    "out",
    "outside",
    "over",
    "overall",
    "own",
    "p",
    "particular",
    "particularly",
    "per",
    "perhaps",
    "placed",
    "please",
    "plus",
    "possible",
    "presumably",
    "probably",
    "provides",
    "q",
    "que",
    "quite",
    "qv",
    "r",
    "rather",
    "rd",
    "re",
    "really",
    "reasonably",
    "regarding",
    "regardless",
    "regards",
    "relatively",
    "respectively",
    "right",
    "s",
    "said",
    "same",
    "saw",
    "say",
    "saying",
    "says",
    "second",
    "secondly",
    "see",
    "seeing",
    "seem",
    "seemed",
    "seeming",
    "seems",
    "seen",
    "self",
    "selves",
    "sensible",
    "sent",
    "serious",
    "seriously",
    "seven",
    "several",
    "shall",
    "she",
    "should",
    "shouldn't",
    "since",
    "six",
    "so",
    "some",
    "somebody",
    "somehow",
    "someone",
    "something",
    "sometime",
    "sometimes",
    "somewhat",
    "somewhere",
    "soon",
    "sorry",
    "specified",
    "specify",
    "specifying",
    "still",
    "sub",
    "such",
    "sup",
    "sure",
    "t",
    "t's",
    "take",
    "taken",
    "tell",
    "tends",
    "th",
    "than",
    "thank",
    "thanks",
    "thanx",
    "that",
    "that's",
    "thats",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "thence",
    "there",
    "there's",
    "thereafter",
    "thereby",
    "therefore",
    "therein",
    "theres",
    "thereupon",
    "these",
    "they",
    "they'd",
    "they'll",
    "they're",
    "they've",
    "think",
    "third",
    "this",
    "thorough",
    "thoroughly",
    "those",
    "though",
    "three",
    "through",
    "throughout",
    "thru",
    "thus",
    "to",
    "together",
    "too",
    "took",
    "toward",
    "towards",
    "tried",
    "tries",
    "truly",
    "try",
    "trying",
    "twice",
    "two",
    "u",
    "un",
    "under",
    "unfortunately",
    "unless",
    "unlikely",
    "until",
    "unto",
    "up",
    "upon",
    "us",
    "use",
    "used",
    "useful",
    "uses",
    "using",
    "usually",
    "uucp",
    "v",
    "value",
    "various",
    "very",
    "via",
    "viz",
    "vs",
    "w",
    "want",
    "wants",
    "was",
    "wasn't",
    "way",
    "we",
    "we'd",
    "we'll",
    "we're",
    "we've",
    "welcome",
    "well",
    "went",
    "were",
    "weren't",
    "what",
    "what's",
    "whatever",
    "when",
    "whence",
    "whenever",
    "where",
    "where's",
    "whereafter",
    "whereas",
    "whereby",
    "wherein",
    "whereupon",
    "wherever",
    "whether",
    "which",
    "while",
    "whither",
    "who",
    "who's",
    "whoever",
    "whole",
    "whom",
    "whose",
    "why",
    "will",
    "willing",
    "wish",
    "with",
    "within",
    "without",
    "won't",
    "wonder",
    "would",
    "would",
    "wouldn't",
    "x",
    "y",
    "yes",
    "yet",
    "you",
    "you'd",
    "you'll",
    "you're",
    "you've",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "z",
    "zero",
]

NOUN = "n"
VERB = "v"
ADV = "r"
ADJ = "a"

class Util:
    """
    Contains a collection of common utility methods.

    """

    @staticmethod
    def sanitize_text(text):
        """
        Returns text after removing unnecessary parts.

        """

        max_word_length = 1024

        _text = " ".join([
            l for l in text.strip().split("\n") if (
                not l.strip().startswith("&gt;")
            )
        ])
        substitutions = [
            (r"$$(.*?)$$$(.*?)$", r""),   # Remove links from Markdown
            (r"[\"](.*?)[\"]", r""),    # Remove text within quotes
            (r" \'(.*?)\ '", r""),      # Remove text within quotes
            (r"\.+", r". "),        # Remove ellipses
            (r"$.*?$", r""),        # Remove text within round brackets
            (r"&amp;", r"&"),         # Decode HTML entities
            (r"http.?:\S+\b", r" ")     # Remove URLs
        ]
        for pattern, replacement in substitutions:
            _text = re.sub(pattern, replacement, _text, flags=re.I)

        # Remove very long words
        _text = " ".join(
            [word for word in _text.split(" ") if len(word) <= max_word_length]
        )
        return _text

    @staticmethod
    def coalesce(l):
        """
        Given a list, returns the last element that is not equal to "generic".

        """

        l = [x for x in l if x.lower() != "generic"]
        return next(iter(l[::-1]), "")

    @staticmethod
    def humanize_days(days):
        """
        Return text with years, months and days given number of days.

        """
        y = days//365 if days > 365 else 0
        m = (days - y*365)//31 if days > 30 else 0
        d = days - m*31 - y*365
        yy = str(y) + " year" if y else ""
        if y > 1:
            yy += "s"
        mm = str(m) + " month" if m else ""
        if m > 1:
            mm += "s"
        dd = str(d) + " day"
        if d>1 or d==0:
            dd += "s"
        return (yy + " " + mm + " " + dd).strip()

    @staticmethod
    def scale(val, src, dst):
        """
        Scale the given value from the scale of src to the scale of dst.
        """
        return ((val - src[0])/(src[1] - src[0])) * (dst[1]-dst[0]) + dst[0]

    @staticmethod
    def decode_if_bytes(obj):
        """
        Convert bytes to str helper function
        """
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        return obj
    
class TextParser:
    """
    Utility class for processing text content.
    """

    substitutions = [
        (r"\b(im|i'm)\b", "i am"),
        (r"\b(ive|i've)\b", "i have"),
        (r"\b(id|i'd)\b", "i would"),
        (r"\b(i'll)\b", "i will"),
        (r"\bbf|b/f\b", "boyfriend"),
        (r"\bgf|g/f\b", "girlfriend"),
        (r"\byoure\b", "you are"),
        (r"\b(dont|don't)\b", "do not"),
        (r"\b(didnt|didn't)\b", "did not"),
        (r"\b(wasnt|wasn't)\b", "was not"),
        (r"\b(isnt|isn't)\b", "is not"),
        (r"\b(arent|aren't)\b", "are not"),
        (r"\b(werent|weren't)\b", "were not"),
        (r"\b(havent|haven't)\b", "have not"),
        (r"\b(couldnt|couldn't)\b", "could not"),
        (r"\b(hadnt|hadn't)\b", "had not"),
        (r"\b(wouldnt|wouldn't)\b", "would not"),
        (r"\bgotta\b", "have to"),
        (r"\bgonna\b", "going to"),
        (r"\bwanna\b", "want to"),
        (r"\b(kinda|kind of)\b", ""),
        (r"\b(sorta|sort of)\b", ""),
        (r"\b(dunno|donno)\b", "do not know"),
        (r"\b(cos|coz|cus|cuz)\b", "because"),
        (r"\bfave\b", "favorite"),
        (r"\bhubby\b", "husband"),
        (r"\bheres\b", "here is"),
        (r"\b(it's)\b", "it is"),
        (r"\b(there's|theres)\b", "there is"),
        (r"\b(where's|wheres)\b", "where is"),
        # Common acronyms, abbreviations and slang terms
        (r"\birl\b", "in real life"),
        (r"\biar\b", "in a relationship"),
        (r"\btotes\b", "totally"),
        (r",", " and "),
        # Remove fluff phrases
        (r"\b(btw|by the way)\b", ""),
        (r"\b(tbh|to be honest)\b", ""),
        (r"\b(imh?o|in my( humble)? opinion)\b", ""),
    ]

    corpus_substitutions = [(r"\b(cant|can't)\b", "cannot"), (r"(\&gt\;)", ">")]

    # Skip if any of these is the *only* attribute - for instance,
    # "I'm a big fan of Queen" makes sense, but "I'm a fan" doesn't.
    skip_lone_attributes = [
        "fan",
        "expert",
        "person",
        "advocate",
        "customer",
    ]

    # A select set of attributes we want to exclude.
    skip_attributes = [
        "supporter",
        "believer",
        "gender",
        "backer",
        "sucker",
        "chapter",
        "passenger",
        "super",
        "water",
        "sitter",
        "killer",
        "stranger",
        "monster",
        "leather",
        "holder",
        "creeper",
        "shower",
        "member",
        "wonder",
        "hungover",
        "sniper",
        "silver",
        "beginner",
        "lurker",
        "loser",
        "number",
        "stupider",
        "outlier",
        "molester",
        "hitler",
        "beer",
        "cucumber",
        "earlier",
        "denier",
        "lumber",
        "hamster",
        "abuser",
        "murderer",
        "dealer",
        "consumer",
        "wallpaper",
        "paper",
        "madder",
        "uber",
        "computer",
        "rubber",
        "door",
        "liquor",
        "traitor",
        "favor",
        "year",
        "ear",
        "liar",
        "rapist",
        "racist",
        "misogynist",
        "apologist",
        "sexist",
        "satan",
        "batman",
        "veteran",
        "ban",
        "hypocrite",
        "candidate",
        "lot",
        "faggot",
        "teapot",
        "shot",
        "foot",
        "idiot",
        "bigot",
        "robot",
    ]

    # A select set of attributes we want to include.
    include_attributes = [
        "geek",
        "nerd",
        "nurse",
        "cook",
        "student",
        "consultant",
        "mom",
        "dad",
        "marine",
        "chef",
        "sophomore",
        "catholic",
        "mod",
        # TODO - These make sense only when accompanied by
        # at least another noun
        # "person","enthusiast","fanboy","player","advocate",
    ]

    # Super awesome logic - if noun ends in any of these, it's *probably*
    # something we want to include/exclude. TODO - This is terrible logic,
    # see if we can implement actual NLP.
    include_attribute_endings = (
        "er",
        "or",
        "ar",
        "ist",
        "an",
        "ert",
        "ese",
        "te",
        "ot",
    )
    exclude_attribute_endings = ("ing", "fucker")

    # "Filler" words (in sentences such as "I think...", "I guess...", etc.)
    skip_verbs = ["were", "think", "guess", "mean"]
    skip_prepositions = ["that"]
    skip_adjectives = ["sure", "glad", "happy", "afraid", "sorry", "certain"]
    skip_nouns = [
        "right",
        "way",
        "everything",
        "everyone",
        "things",
        "thing",
        "mine",
        "stuff",
        "lot",
        "like",
        "love",
    ]

    # Should _N include conjunctions?
    grammar = r"""
    # adverb* verb adverb* 
    # - really think, strongly suggest, look intensely
    _VP:  
      {<RB.*>*<V.*>+<RB.*>*}

    # determiner adjective noun(s)
    # - a beautiful house, the strongest fighter
    _N0:
      {(<DT>*<JJ.*>*<NN.*>+<JJ.*>*(?!<POS>))+}
    _N:
      {<_N0>+}   

    # noun to/in noun 
    # - newcomer to physics, big fan of Queen, newbie in gaming
    _N_PREP_N:
      {<_N>((<TO>|<IN>)<_N>)+}

    # my adjective noun(s) 
    # - my awesome phone
    POSS:
      {<PRP\$><_N>}

    # I verb in* adjective* noun
    # - I am a great chef, I like cute animals
    # - I work in beautiful* New York, I live in the suburbs
    ACT1:
      {<PRP><_VP><IN>*<_N>}

    # Above + to/in noun
    # - I am a fan of Jaymay, I have trouble with flannel
    ACT2:
      {<PRP><_VP><IN>*<_N_PREP_N>}
  """

    chunker = RegexpParser(grammar)

    def download_nltk_resources(self):
        """
        Downloads required NLTK resources if not already present.
        Uses virtual environment path when available.
        """
        # Get the virtual environment path
        if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
            # We're in a virtual environment
            venv_path = sys.prefix
            nltk_data_path = os.path.join(venv_path, 'nltk_data')
        else:
            # Fallback to user directory if not in venv
            nltk_data_path = os.path.join(os.path.expanduser('~'), 'nltk_data')
        
        # Ensure the directory exists
        os.makedirs(nltk_data_path, exist_ok=True)
        
        # Add our venv path to NLTK's data path
        nltk.data.path.insert(0, nltk_data_path)
        
        print(f"Using NLTK data path: {nltk_data_path}")
        
        required_resources = {
            'averaged_perceptron_tagger': ('taggers', 'averaged_perceptron_tagger'),
            'punkt': ('tokenizers', 'punkt'),
            'movie_reviews': ('corpora', 'movie_reviews'),
            'brown': ('corpora', 'brown'),
            'conll2000': ('corpora', 'conll2000')
        }
        
        # Special handling for wordnet
        try:
            wordnet.ensure_loaded()
        except LookupError:
            print("Downloading wordnet...")
            nltk.download('wordnet', download_dir=nltk_data_path)
            try:
                wordnet.ensure_loaded()
                print("Wordnet successfully loaded")
            except:
                print("Warning: Issues with wordnet loading")
        
        # Handle other resources
        for resource, (folder, name) in required_resources.items():
            resource_path = os.path.join(nltk_data_path, folder, name)
            if not os.path.exists(resource_path):
                print(f"Downloading {resource}...")
                nltk.download(resource, download_dir=nltk_data_path, quiet=True)
                if os.path.exists(resource_path):
                    print(f"Successfully downloaded {resource}")
                else:
                    print(f"Warning: {resource} download may have failed")

        # Verify all resources
        print("\nVerifying resources...")
        all_found = True
        
        # Check wordnet separately
        try:
            wordnet.ensure_loaded()
            print("Wordnet verified")
        except:
            print("Warning: Wordnet not properly loaded")
            all_found = False
        
        # Check other resources
        for resource, (folder, name) in required_resources.items():
            resource_path = os.path.join(nltk_data_path, folder, name)
            if not os.path.exists(resource_path):
                print(f"Warning: {resource} not found at {resource_path}")
                all_found = False
            else:
                pass
                # Print if resource is found
                # print(f"Found {resource}")

        
        if all_found:
            print("All resources verified successfully")
        else:
            print("Some resources are missing")

    def clean_up(self, text, substitutions):
        """
        Removes unnecessary words from text and replaces common
        misspellings/contractions with expanded words.

        """

        for original, rep in substitutions:
            text = re.sub(original, rep, text, flags=re.I)
        return text

    def normalize(self, word, tag="N"):
        """
        Normalizes word using given tag. If no tag is given, NOUN is assumed.

        """

        kind = NOUN
        if tag.startswith("V"):
            kind = VERB
        elif tag.startswith("RB"):
            kind = ADV
        elif tag.startswith("J"):
            kind = ADJ
        return Word(word).lemmatize(kind).lower()

    def pet_animal(self, word):
        """
        Returns word if word is in a predefined list of pet animals.

        """

        word = word.lower()
        if re.match(r"\b(dog|cat|hamster|fish|pig|snake|rat|parrot)\b", word):
            return word
        else:
            return None

    def family_member(self, word):
        """
        Returns normalized word if word is in a predefined list
        of family members.

        """

        word = word.lower()
        if re.match(r"\b(mom|mother|mum|mommy)\b", word):
            return "mother"
        elif re.match(r"\b(dad|father|pa|daddy)\b", word):
            return "father"
        elif re.match(r"\b(brother|sister|son|daughter)s?\b", word):
            return word
        else:
            return None

    def relationship_partner(self, word):
        """
        Returns word if word is in a predefined list of relationship partners.

        """

        word = word.lower()
        if re.match(r"\b(ex-)*(boyfriend|girlfriend|so|wife|husband)\b", word):
            return word
        else:
            return None

    def gender(self, word):
        """
        Returns normalized word if word is in a predefined list of genders.

        """

        word = word.lower()
        if re.match(r"\b(girl|woman|female|lady|she)\b", word):
            return "female"
        elif re.match(r"\b(guy|man|male|he|dude)\b", word):
            return "male"
        else:
            return None

    def orientation(self, word):
        """
        Returns word if word is in a predefined list of sexual orientations.

        """

        word = word.lower()
        if re.match(r"\b(gay|straight|bi|bisexual|homosexual)\b", word):
            return word
        else:
            return None

    def process_verb_phrase(self, verb_tree):
        """
        Returns list of (word,tag) tuples given a verb tree.

        """

        if verb_tree.label() != "_VP":
            return None
        verb_phrase = [(w.lower(), t) for w, t in verb_tree.leaves()]
        return verb_phrase

    def process_noun_phrase(self, noun_tree):
        """
        Returns list of (word,tag) tuples given a noun tree.

        """

        if noun_tree.label() != "_N":
            return []
        if any(
            n in self.skip_nouns + stopwords
            for n, t in noun_tree.leaves()
            if t.startswith("N")
        ):
            return []

        noun_phrase = [(w.lower(), t) for w, t in noun_tree.leaves()]
        return noun_phrase

    def process_npn_phrase(self, npn_tree):
        """
        Given a phrase of the form noun-preposition-noun, returns noun
        and preposition-noun phrases.
        """

        if npn_tree.label() != "_N_PREP_N":
            return None

        noun_phrase = []
        prep_noun_phrase = []
        for i, node in enumerate(npn_tree):
            # we have hit the prepositions in a prep noun phrase
            if isinstance(node, tuple):
                w, t = node
                w = w.lower()
                prep_noun_phrase.append((w, t))
            else:
                if prep_noun_phrase:
                    prep_noun_phrase += self.process_noun_phrase(node)
                else:
                    noun_phrase = self.process_noun_phrase(node)

        return (noun_phrase, prep_noun_phrase)

    def process_possession(self, phrase):
        """
        Given a phrase, checks and returns a possession/belonging
        (my <word>) if exists.
        """

        noun_phrase = []

        for i, node in enumerate(phrase):
            if isinstance(node, tuple):  # word can only be pronoun
                w, t = node
                if t == "PRP$" and w.lower() != "my":
                    return None
            else:  # type has to be nltk.tree.Tree
                if node.label() == "_N":
                    noun_phrase = self.process_noun_phrase(node)
                else:  # what could this be?
                    pass

        if noun_phrase:
            return {"kind": "possession", "noun_phrase": noun_phrase}
        else:
            return None


    def process_action(self, phrase):
        """
        Given a phrase, checks and returns an action
        (I <verb-phrase>) if exists.
        """

        verb_phrase = []
        prepositions = []
        noun_phrase = []
        prep_noun_phrase = []

        for i, node in enumerate(phrase):
            if isinstance(node, tuple):  # word is either pronoun or preposition
                w, t = node
                if t == "PRP" and w.lower() != "i":
                    return None
                elif t == "IN":
                    prepositions.append((w.lower(), t))
                else:  # what could this be?!
                    pass
            else:
                if node.label() == "_VP":
                    verb_phrase = self.process_verb_phrase(node)
                elif node.label() == "_N":
                    noun_phrase = self.process_noun_phrase(node)
                elif node.label() == "_N_PREP_N":
                    noun_phrase, prep_noun_phrase = self.process_npn_phrase(node)

        if noun_phrase:
            return {
                "kind": "action",
                "verb_phrase": verb_phrase,
                "prepositions": prepositions,
                "noun_phrase": noun_phrase,
                "prep_noun_phrase": prep_noun_phrase,
            }
        else:
            return None

    def extract_chunks(self, text):
        chunks = []
        sentiments = []
        text = self.clean_up(text, self.substitutions)

        try:
            # Download resources only once at the start
            if not hasattr(TextParser, '_resources_checked'):
                self.download_nltk_resources()
                TextParser._resources_checked = True

            sentences = sent_tokenize(text)
            
            for sent in sentences:
                # Only process sentences containing 'i' or 'my'
                if not re.search(r"\b(i|my)\b", sent, re.I):
                    continue
                    
                # Tokenize and tag the sentence
                tokens = word_tokenize(sent)
                tagged = pos_tag(tokens)
                
                # Parse the chunks using our existing chunker
                tree = self.chunker.parse(tagged)
                
                # Process the chunks with the same filtering as original
                for subtree in tree.subtrees(filter=lambda t: t.label() in ["POSS", "ACT1", "ACT2"]):
                    phrase = [(w.lower(), t) for w, t in subtree.leaves()]
                    phrase_type = subtree.label()

                    # Skip if doesn't contain 'i' or 'my', or contains skip words
                    if not any(x in [("i", "PRP"), ("my", "PRP$")] for x in phrase) or (
                        phrase_type in ["ACT1", "ACT2"] and (
                            any(word in self.skip_verbs 
                                for word in [w for w, t in phrase if t.startswith("V")]) or
                            any(word in self.skip_prepositions 
                                for word in [w for w, t in phrase if t == "IN"]) or
                            any(word in self.skip_adjectives 
                                for word in [w for w, t in phrase if t == "JJ"])
                        )
                    ):
                        continue

                    # Process the chunk based on its type
                    if subtree.label() == "POSS":
                        chunk = self.process_possession(subtree)
                        if chunk:
                            chunks.append(chunk)
                    elif subtree.label() in ["ACT1", "ACT2"]:
                        chunk = self.process_action(subtree)
                        if chunk:
                            chunks.append(chunk)

            return (chunks, sentiments)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return (chunks, sentiments)

    def ngrams(self, text, n=2):
        """
        Returns a list of ngrams for given text.

        """
        return [" ".join(w) for w in TextBlob(text).ngrams(n=n)]

    def noun_phrases(self, text):
        """
        Returns list of TextBlob-derived noun phrases.

        """

        return TextBlob(text).noun_phrases

    def common_words(self, text):
        """
        Given a text, splits it into words and returns as a list
        after excluding stop words. Preserves contractions except 's.
        """
        if not text:
            return []
        
        # First apply all substitutions to expand contractions
        text = self.clean_up(text, self.substitutions)
        
        # Convert to lowercase
        text = text.lower()
        
        # Split into words and filter
        words = text.split()
        
        # Filter out stopwords and short words
        filtered_words = [
            word
            for word in words
            if (word not in stopwords 
                and len(word) > 1
                and word.isalpha())  # Only pure alphabetic words
        ]
        
        return filtered_words

    def total_word_count(self, text):
        """
        Returns total word count of a given text.

        """

        return len(list(TextBlob(text).words))

    def unique_word_count(self, text):
        """
        Returns unique word count of a given text.

        """

        return len(set(list(TextBlob(text).words)))

    def longest_word(self, text):
        """
        Returns longest word in a given text.

        """

        return max((list(TextBlob(text).words)), key=len)

    @staticmethod
    def test_sentence(sentence):
        """
        Prints TextBlob-derived tags for a given sentence.

        For testing purposes only.

        """

        print(TextBlob(sentence).tags)