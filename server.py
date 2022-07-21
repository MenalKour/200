import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

server.bind((ip_address, port))
server.listen()

list_of_clients = []
nicknames = []

questions = [
     " What country has the highest life expectancy? \n a.Hong Kong\n b.India\n c.Pakistan\n d.Russia",
     " WWho was the Ancient Greek God of the Sun? \n a.Apollo\n b.Zeus\n c.Poseidon\n d.Ares",
     " What artist has the most streams on Spotify? \n a.BTS\n b.Drake\n c.Dua Lipa\n d.Katy Perry",
     " What character has both Robert Downey Jr. and Benedict Cumberbatch played? \n a.Iron Man\n b.Dr.Strange\n c.Sherlock Holmes\n d.Batman",
     " Which planet in the Milky Way is the hottest? \n a.Venus\n b.Saturn\n c.Neptune\n d.Mercury",
     " What city is known as The Eternal City? \n a.Rome\n b.Greece\n c.Norway\n d.Italy",
     " What is a group of crows called? \n a.A murder\n b.A fleek\n c.A group\n d.A bunch",
     " Which is the only body part that is fully grown from birth? \n a.Bones\n b.Eyes\n c.Ears\n d.Tongue",
     " What is acrophobia a fear of? \n a.Flying\n b.Water\n c.Height\n d.Ghosts",
     " Who is Loki? \n a.God of Thunder\n b.God of Dwarves\n c.God of Mischief\n d.God of Gods",
     " Who wrote novel Pride and Prejudice? \n a.JK Rowling\n b.Jane Austin\n c.Menal Kour\n d.Both a and c ",
     " Which of the 5 senses is the first to develop? \n a.Taste\n b.Hearing\n c.Sight\n d.Smell",
     " True or False - All people are colorblind when they are born \n a.True\n b.What?\n c.False\n d.Babies?",
     " Who founded Facebook? \n a.Bill Gates\n b.Elon Musk\n c.Mark Zukerberg\n d.Steve Jobs",
     " Which is the longest river on Earth? \n a.Nile\n b.Ganga\n c.Indus\n d.None of these",
     " Who plays the role of Captain America in Marvel Series? \n a.Tom Holland\n b.Chris Evans\n c.Robert Downey Jr\n d.Chris Hemsworth",
     " Which of the following is the world’s largest and deepest ocean? \n a.Pacific\n b.Arctic\n c.Atlantic\n d.Indian"
]

answers = ['a', 'a', 'b', 'c', 'a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'a', 'c', 'a', 'b', 'a']

print("Server has started...")

def get_random_question_answer(conn):
    random_index = random.randint(0,len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You will receive a question. The answer to that question should be one of a, b, c or d!\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    print(answer)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.split(": ")[-1].lower() == answer:
                    score += 1
                    conn.send(f"Bravo! Your score is {score}\n\n".encode('utf-8'))
                else:
                    conn.send("Incorrect answer! Better luck next time!\n\n".encode('utf-8'))
                remove_question(index)
                index, question, answer = get_random_question_answer(conn)
                print(answer)
            else:
                remove(conn)
                remove_nickname(nickname)
        except Exception as e:
            print(str(e))
            continue

def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)

def remove_nickname(nickname):
    if nickname in nicknames:
        nicknames.remove(nickname)

while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    list_of_clients.append(conn)
    nicknames.append(nickname)
    print (nickname + " connected!")
    new_thread = Thread(target= clientthread,args=(conn,nickname))
    new_thread.start()
