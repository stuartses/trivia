from .models import Questions


# insert question to database
def insert_question(question_data):
    new_question = Questions()
    new_question.question = question_data['question']
    new_question.option1 = question_data['option1']
    new_question.option2 = question_data['option2']
    new_question.option3 = question_data['option3']
    new_question.option4 = question_data['option4']
    new_question.answer = question_data['answer']
    new_question.save()


# load questions from databae
def load(question_name):
    question_id = 0
    if (question_name == 'question1'):
        question_id = 1
    if (question_name == 'question2'):
        question_id = 2
    if (question_name == 'question3'):
        question_id = 3

    question = Questions.objects.get(id=question_id)

    return question


# insert default data
def default_data():
    question_data = {
        'question': "Cuál es el lugar más frío de la tierra",
        'option1': "Ártico",
        'option2': "Antártida",
        'option3': "Monte Everest",
        'option4': "Groelandia",
        'answer': "Antártida"
    }
    insert_question(question_data)

    question_data = {
        'question': "Cuál es el río más largo del mundo",
        'option1': "Magdalena",
        'option2': "Nilo",
        'option3': "Misisipi",
        'option4': "Amazonas",
        'answer': "Amazonas"
    }
    insert_question(question_data)

    question_data = {
        'question': "Cuándo acabó la II Guerra Mundial",
        'option1': "1945",
        'option2': "1946",
        'option3': "1940",
        'option4': "1947",
        'answer': "1945"
    }
    insert_question(question_data)
