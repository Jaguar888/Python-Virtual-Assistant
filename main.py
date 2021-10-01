import requests
from bs4 import BeautifulSoup
import random
from textblob import TextBlob
import json
import sys

print("Welcome to your Python virtual assistant. Ask me anything!")


def search():
    query = str(input("\nWhat do you want to search for?\n\n"))
    search = str("https://google.com/search?q=" + query)
    html = requests.get(search).text
    links = []

    aTags = BeautifulSoup(html, 'html.parser').find_all('a')
    for link in aTags:
        href = link.get('href')[7:]
        split_string = href.split("&", 1)
        href = split_string[0]
        if "http" in href and "google" not in href and "wikipedia" not in href and "wikimedia.org" not in href and len(
                links) < 11:
            links.append(href)

    print("\nI found this on the web:\n")
    for i in links:
        print(i)


def britannica():

    query = str(input("\nWhat do you want information about?\n\n"))
    search = str("https://www.google.com/search?q=britannica%20" + query +
                 "&filter=0&")
    html = requests.get(search).text
    bLinks = []
    soup = BeautifulSoup(html, 'html.parser')
    aTags = soup.find_all('a')
    for link in aTags:
        href = link.get('href')[7:]
        split_string = href.split("&", 1)
        href = split_string[0]
        if "https://" in href and "britannica.com" in href:
            bLinks.append(href)
    counter = 0
    response = "no"
    while response == "no":
        bLink = bLinks[counter]
        html = requests.get(bLink).text
        description = str(
            BeautifulSoup(html,
                          'html.parser').find_all("meta",
                                                  property="og:description"))
        description = description[16:-30]
        print("\n" + query, "are/is:\n\n" + description,
              "\n\nSource: " + bLink + "\n\n")
        response = str(
            input(
                "Did you find what you were looking for? Type 'yes' if you did or type 'no' if you didn't.\n\n"
            ))
        if response == "yes":
            print("\nIt was my pleasure helping you.\n")
            break
        elif response == "no":
            if bLink != bLinks[-1]:
                counter = counter + 1
            else:
                print(
                    "\nSorry I couldn't help you. Maybe try different keywords to receive what you want."
                )
                break
        else:
            print("\nI couldn't understand you.")
            break


def chatBot():
    name = input('\nHey, what\'s your name?')

    greetings = [
        'How are you today ' + name + '?',
        'Howdy ' + name + ' how are you feeling?', "What's up " + name + '?',
        'Greetings ' + name + ', are you well?',
        'How are things going ' + name + '?',
        'Hey' + name + 'how is everything going?'
    ]
    print(random.choice(greetings))
    ans = input()
    blob = TextBlob(ans)

    if blob.polarity > 0:
        print('Glad you are doing well')
    else:
        print('Sorry to hear that')

    topics = [
        'football', 'Melbourne', 'AFL', 'Endgame', 'Python', 'school', 'math',
        'science', 'phones'
        'Computers', 'Computer games'
    ]

    questions = [
        'What is your take on ', 'What do you think about ',
        'How do you feel about ', 'What do you reckon about ',
        'I would like your opinion on '
    ]
    for i in range(0, random.randint(3, 4)):
        question = random.choice(questions)
        questions.remove(question)
        topic = random.choice(topics)
        topics.remove(topic)
        print(question + topic + '?')
        ans = input()
        blob = TextBlob(ans)

        if blob.polarity > 0.5:
            print('OMG you really love ' + topic)
        elif blob.polarity > 0.1:
            print('Well, you clearly like ' + topic)
        elif blob.polarity < -0.5:
            print('Woof, you totally hate ' + topic)
        elif blob.polarity < -0.5:
            print("So you don't like " + topic)
        else:
            print('That is a very neutral view on ' + topic)

        if blob.subjectivity > 0.6:
            print('and you are so biased')
        elif blob.subjectivity > 0.3:
            print('and you are a bit biased')
        else:
            print('and you are quite objective')

    #4. Random goodbye

    goodbyes = [
        'Good talking to you ' + name + ' I gotta go now',
        'OK I am bored, I will go watch Netflix', 'Bye bye, I am out',
        'Yaaawn . . . I gotta go now', 'Catch you later, ' + name,
        'See you soon!'
    ]

    print(random.choice(goodbyes))
    print(
        "\n-----------------------------------------------------------------------------"
    )


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    print("\n" + quote + "\n")


def userChoice():
    understood = False
    while understood == False:
        choice = input(
            "\nIf you want learn about something, just type 'information'. If you want to search the web, just type 'google'. If you want to be inspired, type 'inspire me'. Or if you just want to talk, just say 'hi'! Say 'bye' to end.\n\n"
        )
        choice = choice.lower()
        if choice == "google":
            search()
            userChoice()
        elif choice == "hi":
            chatBot()
            userChoice()
        elif choice == "information":
            britannica()
            userChoice()
        elif choice == "inspire me":
            get_quote()
            userChoice()

        elif choice == "bye":
            goodbyes = [
                'Catch you later!', 'Goodbye!', 'Bye!', 'Enjoy your day!',
                'It was great talking to you!', 'See you soon!'
            ]

            print("\n" + random.choice(goodbyes))
            try:
                break
            finally:
                sys.exit()

        else:
            print("\nI could not understand you.")
            userChoice()


userChoice()
