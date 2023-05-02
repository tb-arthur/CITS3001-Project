from agents import *
from collections import defaultdict
import random
import csv
import matplotlib.pyplot as plt
import networkx as nx
import igraph as ig

ELECTION_DAY = 7
N = 37
ENERGY_LEVEL = 100

def populate_teams(file):
    '''
    initializes green, blue and red team along with their designated 
    number of agents from a given file
    
    @param String file: file that contains information on the population of the teams
    --> use dict reader
    '''
    global green
    global grey_good
    global grey_bad

    green_agents = []
    grey_agents_good = []
    grey_agents_bad = []

    agent_population = {}
    population_file = open(file, 'r')
    with population_file as file:
        csv.register_dialect('dialect', delimiter=',')
        contents = csv.DictReader(file, dialect='dialect')
        for row in contents:
            team_id = int(row['id'])
            team_color = str(row['team'])
            agent_population.update({team_id : team_color})

    for id,color in agent_population.items():
        if color == "green":
            green_agents.append(id)

        elif color == "blue":
            global blue
            blue = Blue(id, ENERGY_LEVEL)
        
        elif color == "red":
            global red
            red = Red(id)
        
        elif color.startswith("grey"):
            if "good" in color:
                grey_agents_good.append(id)
            else:
                grey_agents_bad.append(id)

    green = {id: Green(id) for id in green_agents}
    grey_good = {id: Grey(id, "good") for id in grey_agents_good}
    grey_bad = {id: Grey(id, "bad") for id in grey_agents_bad}
    
    print("Green agent ID's:")
    for agent in green:
        #   X -> Opinion, U -> Uncertainty
        print(f"Green: {green[agent].id}, X: {green[agent].vote}, U: {green[agent].uncertainty}")
    
    print("\nGrey agent ID's and Teams:")
    for agent in grey_good:
        print(f"{grey_good[agent].id, grey_good[agent].team}")
    for agent in grey_bad:
        print(f"{grey_bad[agent].id, grey_bad[agent].team}")

    print("\nBlue agent ID and Energy:")
    print(f"{blue.id, blue.energy}\n")

    print("Red agent ID:")
    print(f"{red.id}\n")

    generate_adjlist('network-2.csv')
    #print(adj_list.items)

def generate_adjlist(file):
    '''
    generates an adjacency list from the given network-2.csv file
    
    @param String file: file that contains information on connections between nodes
    '''
    global adj_list

    adj_list = defaultdict(set)
    adj_file = open(file)
    next(adj_file)
    with adj_file as f:
        for line in f:
            start, end = line.split(",")
            adj_list[int(start)].add((int(end)))
            adj_list[int(end)].add((int(start)))

def generate_graph(n):
    '''
    generates an Erdos Renyi graph given number of 
    nodes n and probability p

    @param int n:   number of vertices/nodes
    '''
    
    p = random.random()
    seed = 20160

    G = nx.erdos_renyi_graph(n, p)
 
    # print("adjacency list")
    # for line in nx.generate_adjlist(G):
    #     print(line)
    
    print(f"\n{G}")
    nx.draw(G, with_labels=True)
    #plt.show()

def start_game():
    '''
    starts a new game
    '''
    global days         # will be used to track how many rounds have passed
    days = 0
    while(days != ELECTION_DAY and blue.energy != 0):
        if blue.energy == 0:
            print(f"\nBlue agent has depleted its energy! Blue team loses!\n")
            break
        next_round()
    end_game()

def next_round():
    '''
    function used to run all the teams turns.
    '''
    global days
    global changed_votes
    print(f"It's now day {days+1}!")
    days += 1
    blue.blue_turn(green)
    changed_votes = red.red_turn(green)

def end_game():
    '''
    displays which team won, how many green agents decided to vote/not vote
    and exits the game.
    uses ANSI escape code to italicize and change color of some words [https://ozzmaker.com/add-colour-to-text-in-python/]
    '''
    print("\n\t\t\t---\033[1;3mELECTION DAY\033[0m---\n")
    print("It's election day! Let's see how many of the green agents decided to vote!\n")
    
    green_voters = 0
    for agent in green:
        if green[agent].vote == True:
            green_voters += 1

    green_members = len(green)
    green_no_vote = green_members - green_voters

    print(f"Of the {green_members} green agents, {green_voters} agents decided to vote and {green_no_vote} did not!")
    print(f"The ratio of voters to non-voters is: {round((green_voters/green_no_vote), 3)}\n")

    if green_voters > green_no_vote:
        print(f"\033[1;4;34mBlue\033[0m team won! They had {blue.energy} energy remaining!\n")
    else:
        print(f"\033[1;4;31mRed\033[0m team won! They successively changed the votes of {changed_votes} green agents!\n")

def main():
    generate_graph(N)
    populate_teams('node-attributes')
    start_game()

if __name__ == "__main__":
    main()