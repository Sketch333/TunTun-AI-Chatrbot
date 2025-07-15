import aiml
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from glob import glob
from nltk.corpus import wordnet as wn
from nltk import pos_tag, ne_chunk, sent_tokenize, word_tokenize
from nltk.tree import Tree
from nltk.sentiment import SentimentIntensityAnalyzer
import pytholog as pl
import calendar
from datetime import date
from neo4j import GraphDatabase
import hashlib
import re
import dns.resolver
from dateutil import parser
from datetime import datetime
import os
from pos_tags import pos_tags_dict
import requests
from threading import Thread

#
# import nltk
# nltk.download('maxent_ne_chunker_tab')
# nltk.download('averaged_perceptron_tagger_eng')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('wordnet')
# nltk.download('words')
# nltk.download('omw-1.4')
# nltk.download('vader_lexicon')
mood = ""


def connect_neo4j():
    # Define the Neo4j connection details
    uri = "bolt://localhost:7687"
    username = "neo4j"
    password = "test1234"
    # Create a Neo4j driver instance
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def validate_data(email, password):
    driver = connect_neo4j()
    neo4j_session = driver.session()

    query = """
 MATCH (u:User{email:$email, password:$password})
 RETURN u
 """
    password = hash_password(password)
    user = neo4j_session.run(query, email=email, password=password).data()
    neo4j_session.close()
    driver.close()
    if user:
        return True

    return False


def check_email(email):
    driver = connect_neo4j()
    neo4j_session = driver.session()
    query = """
    MATCH (u:User{email:$email})
    RETURN u
    """
    user = neo4j_session.run(query, email=email).data()
    neo4j_session.close()
    driver.close()
    if user:
        print(user)
        return True
    return False


def is_valid_domain(email):
    domain = email.split("@")[1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        return False


def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_email(email):
    if is_valid_email(email) and is_valid_email(email):
        return True
    return False


def get_username(email):
    driver = connect_neo4j()
    neo4j_session = driver.session()
    query = """
    MATCH (u:User{email: $email}) RETURN u.name
    """
    username = neo4j_session.run(query, email=email).data()[0]['u.name']
    neo4j_session.close()
    driver.close()
    return username


def store_credentials(name, email, password):
    password = hash_password(password)
    driver = connect_neo4j()
    neo4j_session = driver.session()

    query = """
    MERGE (u:User{name:$name, email:$email, password:$password})
    """
    neo4j_session.run(query, name=name, email=email, password=password)
    neo4j_session.close()
    driver.close()

    # Create empty facts file for the user
    fact_dir = "prolog/facts"
    os.makedirs(fact_dir, exist_ok=True)  # Ensure directory exists

    fact_path = os.path.join(fact_dir, f"{email.replace('@', '_at_')}.pl")
    with open(fact_path, "w") as f:
        f.write(f"% Facts for {email}\n")
        f.close()

    return


def store_query(prompt, response):
    driver = connect_neo4j()
    neo4j_session = driver.session()
    query = """
    MERGE (q:Query{prompt:$prompt, response:$response})
    """
    neo4j_session.run(query, prompt=prompt, response=response)
    neo4j_session.close()
    driver.close()
    return


def sentiment_analysis(text):
    global mood
    sia = SentimentIntensityAnalyzer()
    results = sia.polarity_scores(text)
    if results['pos'] > results['neg']:
        myBot.setPredicate("sentiment", "positive")
        mood = "positive"
        return
    elif results['neg'] > results['pos']:
        myBot.setPredicate("sentiment", "negative")
        mood = "negative"
        return

    return


def check_sentiment(sentiment):
    pos = pos_tag([sentiment])
    entity = ne_chunk(pos)
    if isinstance(entity[0], Tree):  # Ensure it's a tree (named entity)
        entity_label = entity[0].label()
        if pos[0][1] == "NNP" and (entity_label == 'GPE' or entity_label == 'PERSON'):
            myBot.setPredicate("username", sentiment)
            myBot.setPredicate("sentiment", "")
            return  # Exit the function since the name is recognized

    sentiment_analysis(sentiment)
    return


def set_sentiment():
    global mood
    sentiment = myBot.getPredicate("sentiment")
    if sentiment == "":
        myBot.setPredicate("sentiment", mood)
        return
    return


def get_description(word):
    description = '\n'
    sn = wn.synsets(word)
    length = len(sn)
    for i in range(length):
        # description += str(i+1)
        description += str(i + 1) + ". " + sn[i].definition()
        if i + 1 != length:
            description += '\n'

    return description


def check_meanings(word):
    if word == "":
        myBot.setPredicate("description", "I don't know.")
        return
    else:
        myBot.setPredicate("description", get_description(word))
        word = word.capitalize()
        myBot.setPredicate("word", word)
        return


def find_dob(person_name):
    person_name = person_name.lower() if person_name != "USER" else session["username"].lower()
    myBot.setPredicate("person", person_name.capitalize())
    query = f"dob({person_name}, (Y, M, D))"
    try:
        result = kb.query(pl.Expr(query))
        if result is None:
            result = ['No']
    except Exception as e:
        result = ['No']
    if result[0] != 'No':
        entry = result[0]  # pytholog returns a list of dicts
        raw_year = entry['Y']
        year = int(raw_year.replace('date', '').strip())
        month = int(entry['M'])
        day = int(entry['D'])

        # Convert month number to month name
        month_name = calendar.month_name[month]

        formatted_dob = f"{day} {month_name} {year}"
        myBot.setPredicate("dob", formatted_dob)
        myBot.setPredicate("dob_person", "")
        return
    else:
        myBot.setPredicate("dob", "unknown")
        myBot.setPredicate("dob_person", "")
        return


def find_age(person_name):
    person_name = person_name.lower() if person_name != "USER" else session["username"].lower()
    myBot.setPredicate("person", person_name.capitalize())
    query = f"dob({person_name}, (Y, M, D))"
    print(query)
    try:
        result = kb.query(pl.Expr(query))
        if result is None:
            result = ['No']
    except Exception as e:
        result = ['No']  # Assuming 'kb' is your pytholog KnowledgeBase object
    if result[0] != 'No':
        entry = result[0]
        raw_year = entry['Y']
        year = int(raw_year.replace('date', '').strip())
        month = int(entry['M'])
        day = int(entry['D'])

        today = date.today()
        age = today.year - year - ((today.month, today.day) < (month, day))
        myBot.setPredicate("age", str(age))  # Store age as string
        myBot.setPredicate("age_person", "")  # Clear old stored person if needed
        return
    else:
        myBot.setPredicate("age", "unknown")
        myBot.setPredicate("age_person", "")
        return


def find_gender(person_name):
    person_name = person_name.lower() if person_name != "USER" else session["username"].lower()
    myBot.setPredicate("person", person_name.capitalize())
    # First try male query
    query_male = pl.Expr(f"male({person_name})")
    try:
        result_male = kb.query(query_male)
        if result_male is None:
            result_male = ['No']
    except Exception as e:
        result_male = ['No']

    if result_male and result_male[0] != 'No':
        myBot.setPredicate("gender", "male")
        myBot.setPredicate("gender_person", person_name)
        return

    # If not male, try female query
    query_female = pl.Expr(f"female({person_name})")
    try:
        result_female = kb.query(query_female)
        if result_male is None:
            result_female = ['No']
    except Exception as e:
        result_female = ['No']

    if result_female and result_female[0] != 'No':
        myBot.setPredicate("gender", "female")
        myBot.setPredicate("gender_person", person_name)
        return

    # If neither male nor female found
    myBot.setPredicate("gender", "unknown")
    myBot.setPredicate("gender_person", person_name)
    return


def prompt_check():
    username = session.get('username', '').lower()
    keys = [
        "mood", "word", "dob_person", "age_person", "gender_person",
        "rel", "person1", "gender", "dob", "relation", "person",
        "other_dob_person", "other_dob", "other_gender_person", "other_gender",
        "other_person1", "other_person2", "other_relation"
    ]

    values = {key: myBot.getPredicate(key).strip() for key in keys}

    if values["word"]:
        check_meanings(values["word"])

    if values["mood"]:
        check_sentiment(values["mood"])

    if values["dob_person"]:
        find_dob(values["dob_person"])

    if values["age_person"]:
        print(values["age_person"])
        find_age(values["age_person"])

    if values["gender_person"]:
        print(values["gender_person"])
        find_gender(values["gender_person"])

    if values["rel"] or values["person1"]:
        check_relation(values["rel"], values["person1"])
    if values["other_person1"] and values["other_person2"] and values["other_relation"]:
        append_relation_fact(values["other_person1"], values["other_person2"], values["other_relation"])
    if values["gender"]:
        append_gender_fact(username, values["gender"])
    if values["other_gender_person"] and values["other_gender"]:
        append_gender_fact(values["other_gender_person"], values["other_gender"])
    if values["dob"]:
        append_dob_fact(username, values["dob"])
    if values["other_dob"] and values["other_dob_person"]:
        append_dob_fact(values["other_dob_person"], values["other_dob"])
    if values["relation"] == "married" and values["person1"]:
        append_relation_fact(username, values["person1"], values["relation"])
    if values["relation"] != "married" and values["person"]:
        append_relation_fact(username, values["person"], values["relation"])


def find_person(x, rel):
    expr = f"{rel}(Y,{x})"
    print(expr)
    try:
        result = kb.query(pl.Expr(expr))
        if result is None:
            result = ['No']
    except Exception as e:
        result = ['No']
    print(result)
    if result[0] != 'No':  # If result is not None or empty
        return result[0]["Y"]
    else:
        return "unknown"


def check_relation(rel, person1):
    rel = rel.lower()
    if rel == "" or person1 == "":
        return
    if person1 == "USER":
        person1 = session["username"].lower()
    if rel == "husband" or rel == "wife":
        rel = "married"
    person2 = find_person(person1, rel).capitalize()
    if person2 == "":
        myBot.setPredicate("person2", "unknown")
    else:
        myBot.setPredicate("person2", person2)
        return


def append_gender_fact(username, gender):
    fact = f"{gender.lower()}({username.lower()}).\n"  # example: male(burhan).

    print("Appending gender to Prolog file:", fact)

    fact_file_path = session.get("fact_file")  # get path from session

    if fact_file_path:
        with open(fact_file_path, "a") as f:  # 'a' mode for append
            f.write(fact)
            f.close()
    else:
        print("Fact file path not found in session.")


def append_dob_fact(username, dob):
    """
    Accepts natural date strings like:
    '12 nov 2024', '12 November 2024', '12/10/2024', '12-10-2024'
    and writes to fact file as: dob(username,date(YYYY,MM,DD)).
    """
    try:
        # Parse with dateutil (very flexible)
        date_obj = parser.parse(dob, dayfirst=True)  # dayfirst helps with DD/MM/YYYY format

        year, month, day = date_obj.year, date_obj.month, date_obj.day
        fact = f"dob({username.lower()},date({year},{month},{day})).\n"
        print("Appending to Prolog facts:", fact)

        # Append to fact file from session
        fact_file_path = session.get("fact_file")
        if fact_file_path:
            with open(fact_file_path, "a") as f:
                f.write(fact)
                f.close()
        else:
            print("Error: fact_file not found in session.")

    except Exception as e:
        print("Error parsing or writing DOB:", e)


def append_relation_fact(username, person1, relation):
    # if relation.lower() == "mother" or relation.lower() == "father":
    #     fact1 = f"parent({person1.lower()},{username.lower()}).\n"
    #     fact2 = f"{relation.lower()}({person1.lower()},{username.lower()}).\n"
    #     print("Appending relation to Prolog file:", fact1)
    #
    #     fact_file_path = session.get("fact_file")  # get path from session
    #
    #     if fact_file_path:
    #         with open(fact_file_path, "a") as f:  # 'a' mode for append
    #             f.write(fact1)
    #             f.write(fact2)
    #     else:
    #         print("Fact file path not found in session.")
    #
    # else:
    #     fact = f"{relation.lower()}({username.lower()},{person1.lower()}).\n"

    fact = f"{relation.lower()}({person1.lower()},{username.lower()}).\n"
    print("Appending relation to Prolog file:", fact)
    fact_file_path = session.get("fact_file")  # get path from session

    if fact_file_path:
        with open(fact_file_path, "a") as f:  # 'a' mode for append
            f.write(fact)
            f.close()
    else:
        print("Fact file path not found in session.")
    return None


def save_sensory_memory(text):
    # Get IP address from Flask request context
    ip_address = get_public_ip()
    timestamp = datetime.now().isoformat()
    print(ip_address, timestamp)
    # Assuming Neo4j driver connection already established
    driver = connect_neo4j()
    neo4j_session = driver.session()
    print("Connected to Neo4j")

    # Sentence Tokenization
    sentences = sent_tokenize(text)

    # Create root text node
    neo4j_session.run("""
            MERGE (t:Text:SensoryMemory {full_text: $text, timestamp:$timestamp, ip_address: $ip_address})
        """, text=text, timestamp=timestamp, ip_address=ip_address)

    prev_sentence = None
    for i, sentence in enumerate(sentences):
        # Create sentence node and relationship to text
        neo4j_session.run("""
            MATCH (t:Text:SensoryMemory {full_text: $text})
            MERGE (s:Sentence:SensoryMemory {sentence_text: $sentence})
            MERGE (t)-[:HAS_A_SENTENCE]->(s)
        """, text=text, sentence=sentence)

        # Create NEXT_SENTENCE relationship
        if prev_sentence:
            neo4j_session.run("""
                MATCH (s1:Sentence {sentence_text: $prev_sentence}), (s2:Sentence {sentence_text: $curr_sentence})
                MERGE (s1)-[:NEXT_SENTENCE]->(s2)
            """, prev_sentence=prev_sentence, curr_sentence=sentence)

        prev_sentence = sentence

        # Word Tokenization and HAS_A_WORD, NEXT_WORD relationships
        words = word_tokenize(sentence)
        prev_word = None
        for word in words:
            neo4j_session.run("""
                MATCH (s:Sentence {sentence_text: $sentence})
                MERGE (w:Word:SensoryMemory {word_text: $word})
                MERGE (s)-[:HAS_A_WORD]->(w)
            """, sentence=sentence, word=word)

            if prev_word:
                neo4j_session.run("""
                    MATCH (w1:Word {word_text: $prev_word}), (w2:Word {word_text: $curr_word})
                    MERGE (w1)-[:NEXT_WORD]->(w2)
                """, prev_word=prev_word, curr_word=word)

            prev_word = word

    neo4j_session.close()
    driver.close()


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return None


def save_semantic_memory(text):
    words = word_tokenize(text)
    tagged_words = pos_tag(words)

    driver = connect_neo4j()
    neo4j_session = driver.session()

    for word, tag in tagged_words:
        wn_pos = get_wordnet_pos(tag)
        if wn_pos:
            synsets = wn.synsets(word, pos=wn_pos)
            if synsets:
                synset = synsets[0]
                definition = synset.definition()
                synonyms = set(lemma.name() for lemma in synset.lemmas())
                antonyms = set(ant.name() for lemma in synset.lemmas() for ant in lemma.antonyms())

                # Save Description
                neo4j_session.run("""
                    MERGE (d:Description:SemanticMemory {description: $definition})
                    WITH d MATCH (w:Word:SensoryMemory {word_text: $word})
                    MERGE (w)-[:REFERS_TO]->(d)
                """, word=word, definition=definition)

                # Save Synonyms
                for synonym in synonyms:
                    neo4j_session.run("""
                        MERGE (s:Synonym:SemanticMemory {synonym: $synonym})
                        WITH s MATCH (w:Word:SensoryMemory {word_text: $word})
                        MERGE (w)-[:HAS_SYNONYM]->(s)
                    """, word=word, synonym=synonym)

                # Save Antonyms
                for antonym in antonyms:
                    neo4j_session.run("""
                        MERGE (a:Antonym:SemanticMemory {antonym: $antonym})
                        WITH a MATCH (w:Word:SensoryMemory {word_text: $word})
                        MERGE (w)-[:HAS_ANTONYM]->(a)
                    """, word=word, antonym=antonym)

                # Save IS_A relationship (first hypernym if available)
                hypernyms = synset.hypernyms()
                if hypernyms:
                    hyper = hypernyms[0].lemmas()[0].name()
                    neo4j_session.run("""
                                    MERGE (c:Category:SemanticMemory {name: $hypernym})
                                    WITH c MATCH (w:Word:SensoryMemory {word_text: $word})
                                    MERGE (w)-[:IS_A]->(c)
                                """, word=word, hypernym=hyper)
                # Extract and save Domain (e.g., "food" from "noun.food")
                domain = synset.lexname().split(".")[-1]
                neo4j_session.run("""
                    MERGE (d:Domain:SemanticMemory {domain_name: $domain})
                    WITH d MATCH (w:Word:SensoryMemory {word_text: $word})
                    MERGE (w)-[:BELONGS_TO_DOMAIN]->(d)
                """, word=word, domain=domain)

    neo4j_session.close()
    driver.close()


def extract_named_entities_from_words(words):
    named_entities = []
    pos = pos_tag(words)
    ne_tree = ne_chunk(pos)
    for subtree in ne_tree:
        if isinstance(subtree, Tree):
            entity_name = " ".join([token for token, _ in subtree.leaves()])
            entity_type = subtree.label()
            named_entities.append((entity_name, entity_type))
    return named_entities


def classify_sentence_type(sentence):
    words = word_tokenize(sentence)
    tags = pos_tag(words)

    if not words:
        return "unknown"

    first_word = words[0].lower()
    first_tag = tags[0][1] if tags else ""

    # Interrogative if sentence starts with wh-word or auxiliary/modal verb
    wh_words = {"what", "when", "where", "who", "why", "how", "which", "whom", "whose"}
    aux_modals = {"is", "are", "was", "were", "do", "does", "did", "can", "could", "will", "would", "should", "shall",
                  "may", "might", "have", "has", "had"}

    if first_word in wh_words or first_word in aux_modals:
        return "interrogative"

    # Imperative: usually starts with base form verb (VB) and no subject (PRP/NOUN)
    if first_tag == "VB" and all(tag[1] not in {"PRP", "NN", "NNP"} for tag in tags[:2]):
        return "imperative"

    # Exclamatory: begins with interjection (UH) or exclamatory adjective/adverb
    if first_tag == "UH" or first_word in {"what", "how"} and len(tags) > 1 and tags[1][1] in {"JJ", "RB"}:
        return "exclamatory"

    # Default fallback
    return "declarative"


def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unknown"


def get_location_from_ip(ip=get_public_ip()):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()

        return data.get("city", "Unknown"), data.get("country", "Unknown")
    except:
        return "Unknown", "Unknown"

def recall_sentences_about(keyword):
    driver = connect_neo4j()
    neo4j_session = driver.session()

    results = neo4j_session.run("""
        MATCH (s:Sentence:SensoryMemory)-[:HAS_A_WORD]->(w:Word:SensoryMemory)
        WHERE toLower(w.word_text) CONTAINS toLower($keyword)
        RETURN DISTINCT s.sentence_text AS sentence
        LIMIT 5
    """, keyword=keyword)

    sentences = [record["sentence"] for record in results]
    neo4j_session.close()
    driver.close()

    return sentences

def user_asked_for_memory(msg):
    recall_triggers = [
        "what did i say", "remind me", "earlier i said",
        "recall", "remember when", "past", "mentioned"
    ]
    return any(phrase in msg.lower() for phrase in recall_triggers)



def save_pam_from_sensory_memory(text):
    driver = connect_neo4j()
    neo4j_session = driver.session()
    sia = SentimentIntensityAnalyzer()
    ip_address = get_public_ip()
    city, country = get_location_from_ip(ip_address)

    sentences = sent_tokenize(text)

    for sentence in sentences:
        result = neo4j_session.run("""
            MATCH (s:Sentence:SensoryMemory {sentence_text: $sentence})
            RETURN s
        """, sentence=sentence)

        if result.peek() is None:
            print(f"[SKIPPED] Sentence not found in sensory memory: {sentence}")
            continue

        # Sentiment
        sentiment_score = sia.polarity_scores(sentence)
        sentiment = "positive" if sentiment_score["pos"] > sentiment_score["neg"] else "negative" if sentiment_score[
                                                                                                         "neg"] > \
                                                                                                     sentiment_score[
                                                                                                         "pos"] else "neutral"
        neo4j_session.run("""
            MERGE (se:Sentiment:PerceptualAssociativeMemory {sentiment: $sentiment})
            WITH se MATCH (s:Sentence:SensoryMemory {sentence_text: $sentence})
            MERGE (s)-[:HAS_SENTIMENT]->(se)
        """, sentence=sentence, sentiment=sentiment)

        # Sentence Type
        sentence_type = classify_sentence_type(sentence)
        neo4j_session.run("""
            MERGE (t:SentenceType:PerceptualAssociativeMemory {type: $type})
            WITH t MATCH (s:Sentence:SensoryMemory {sentence_text: $sentence})
            MERGE (s)-[:HAS_TYPE]->(t)
        """, sentence=sentence, type=sentence_type)

        # IP + Location
        neo4j_session.run("""
            MERGE (ip:IPAddress:PerceptualAssociativeMemory {ip: $ip})
            MERGE (loc:Location:PerceptualAssociativeMemory {city: $city, country: $country})
            WITH ip, loc
            MATCH (s:Sentence:SensoryMemory {sentence_text: $sentence})
            MERGE (s)-[:ORIGINATED_FROM]->(ip)
            MERGE (ip)-[:GEO_LOCATED_AT]->(loc)
        """, sentence=sentence, ip=ip_address, city=city, country=country)

        # POS Tags
        words = word_tokenize(sentence)

        pos_tags = pos_tag(words)
        for word, pos in pos_tags:
            long_pos = pos_tags_dict.get(pos, "Unknown")
            neo4j_session.run("""
                MERGE (p:POSTag:PerceptualAssociativeMemory {short: $pos, long: $long_pos})
                WITH p MATCH (w:Word:SensoryMemory {word_text: $word})
                MERGE (w)-[:HAS_POS_TAG]->(p)
            """, word=word, pos=pos, long_pos=long_pos)

        # Named Entities
        named_entities = extract_named_entities_from_words(words)
        for entity_name, entity_type in named_entities:
            neo4j_session.run("""
                MERGE (ne:NamedEntity:PerceptualAssociativeMemory {entity_text: $entity_name, entity_type: $entity_type})
                WITH ne MATCH (s:Sentence:SensoryMemory {sentence_text: $sentence})
                MERGE (s)-[:HAS_NAMED_ENTITY]->(ne)
            """, sentence=sentence, entity_name=entity_name, entity_type=entity_type)

    neo4j_session.close()
    driver.close()


def async_save_all(text):
    try:
        save_sensory_memory(text)
        save_semantic_memory(text)
        save_pam_from_sensory_memory(text)
    except Exception as e:
        print(f"[ASYNC ERROR]: {e}")


kb = pl.KnowledgeBase("family")
kb.clear_cache()
kb.from_file("prolog/kb.pl")

myBot = aiml.Kernel()
app = Flask(__name__)
app.secret_key = 'your-secret-key'
aiml_files = glob("aiml files/*.aiml")
for file in aiml_files:
    myBot.learn(file)


# myBot.learn('aiml files/conversation.aiml')
# myBot.learn('aiml files/jokes.aiml')


@app.route("/")
def home():
    if 'email' in session and 'username' in session:
        return render_template("home.html", username=session['username'])
    else:
        return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        if validate_data(email, password):
            session["email"] = email
            session["username"] = get_username(email)  # Make sure this function exists
            fact_path = os.path.join("prolog/facts", f"{email.replace('@', '_at_')}.pl")
            session["fact_file"] = fact_path
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Invalid credentials")

    # Handle GET requests with query parameters
    error = request.args.get('error')
    success = request.args.get('success')
    return render_template('login.html', error=error, success=success)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if the passwords match
        if password != confirm_password:
            return redirect(url_for('signup') + '?error=password_mismatch')

        if check_email(email):
            print(check_email(email))
            return redirect(url_for('signup') + '?error=email_exists')
        if not validate_email(email):
            return redirect(url_for('signup') + '?error=invalid_email')
        store_credentials(name, email, password)
        return redirect(url_for('login') + '?success=signup')

    return render_template('signup.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/get")
def get_bot_response():
    if "email" not in session:
        return "Please log in to use the bot."
    kb.from_file(session["fact_file"])
    query = request.args.get('msg')
    # save_sensory_memory(query)
    # save_semantic_memory(query)
    # save_pam_from_sensory_memory(query)
    # print(query)
    # Load the user's KB (facts + rules)
    # User-specific facts
    # Check if user wants to recall something
    if user_asked_for_memory(query):
        words = word_tokenize(query)
        for word in words:
            matches = recall_sentences_about(word)
            if matches:
                return "Here's what you said about that:\n" + "\n".join(f"- {m}" for m in matches)
        return "I checked your memory but couldn't find anything relevant."
    Thread(target=async_save_all, args=(query,)).start()
    myBot.respond(query)
    prompt_check()
    response = myBot.respond(query)
    set_sentiment()
    print(myBot.respond(query))
    for key in [
        "mood", "word", "dob_person", "age_person", "gender_person",
        "rel", "person1", "gender", "dob", "relation", "person",
        "other_dob_person", "other_dob", "other_gender_person", "other_gender",
        "other_person1", "other_person2", "other_relation"
    ]:
        myBot.setPredicate(key, "")

    return response


if __name__ == "__main__":
    import webbrowser
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(host="0.0.0.0", port=5000)
