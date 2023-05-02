'''
CITS3001 - Project 2022: A Game on Operations in the Information Environment

    ------- MADE BY: -------
        Sean Lim            22321345
Athhar Daffa Djajasantosa   22676919
'''
from agents import *
from tabulate import tabulate as tb
from statistics import mean
import time
import random
import matplotlib.pyplot as plt
import networkx as nx

SEED = 7727
ENERGY_LEVEL = 100      # default energy level for blue

def generate_network(num_nodes):
    '''
    Generates the base network for the Agents.
    In this function, green and Grey Agents will be added to the graph before Red and Blue Agents.

    @param int  num_nodes: number of nodes (Green Agents) for the initial graph.
    '''
    global updated_graph, color_map, initial_nodes, green, grey, grey_population

    initial_nodes = num_nodes

    prob = random.random()      # generates a float random probability (between 0 and 1) for ER graph
    if VERBOSE:
        print(f"Probability of edges formed: {prob}")

    network_graph = nx.erdos_renyi_graph(n=num_nodes, p=prob, seed=SEED, directed=False)    # generates an ER graph based on number of nodes and probability
    green = {id: Green(id) for id in network_graph}     # initializes Green Agents in graph

    color_map = []
    for node in network_graph:      # initializes color for the graph, starting with Green first
        color_map.append('green')
        
    grey = {}   # dictionary that will contain Grey Agents
    grey_population = int(initial_nodes/9)
    updated_graph, grey = add_grey(network_graph, grey, grey_population)

    updated_graph = add_agents(updated_graph)   # updated graph with Red and Blue agents added
    if VERBOSE:    
        nx.draw_shell(
                updated_graph, 
                node_color=color_map,
                with_labels=True, 
                node_size=1000
                )
        plt.show()      # visualization of graph
        plt.clf()       # clears the current graph

def add_grey(g, grey_dict, grey_pop):
    '''
    Separate function for initializing grey agents and adding them to the graph.

    @param Graph    g: graph that the Grey Agents will be added to.
    @param dict     grey_dict: dictionary which will be populated with Grey Agents.
    @param int      grey_pop: int value that shows how many grey agents to be made.

    @return Graph   g: updated graph that has Grey Agents added to it.
    @return dict    grey_dict: dictionary that has been populated with Grey Agents.
    '''
    global grey_keys

    grey_keys = []      # list which will contain ID's of Grey Agents

    for agent_id in range(grey_pop):
        color_map.append('grey')
        new_id = initial_nodes + agent_id
        grey_dict[new_id] = Grey(new_id)    # initialize Grey Agent
        
        g.add_node(grey_dict[new_id])
        grey_keys.append(new_id)
        g = nx.relabel_nodes(g, {grey_dict[new_id]:'Grey'+str(new_id)})

    return g, grey_dict

def add_agents(g):
    '''
    Initializes the Blue and Red Agents and adds them to the graph.
    If user chose to play as Blue Agent, game will prompt user to input an energy for the Blue Agent.

    @param  Graph    g: graph that the Blue and Red Agents will be added to.

    @return Graph   g: updated graph that has added Blue and Red Agents plus their colors.
    '''
    global blue, red

    energy = ENERGY_LEVEL
    if player_team == 'Blue':       # check if player chose to play as Blue Agent
        energy = input("Please choose a base value for Blue Agents starting energy!\n")
        if energy == "":      # ELECTION_DAY defaults to a value between 23 and 31 if no input is given
            energy = 100*5
    color_map.append('blue')
    blue_id = g.number_of_nodes() + 1
    blue = Blue(blue_id, int(energy)*5)    # initialization of Blue Agent

    color_map.append('red')
    red_id = blue_id + 1
    red = Red(red_id)                 # initialization of Red Agent

    g.add_node(blue)
    g.add_node(red)

    for node in g:                    # connect Blue to every voting Agent, Red to every Green Agent
        if type(node) != int:
            break
        g.add_edge(red, node)
        if green[node].vote == True:
            g.add_edge(blue, node)
        
    g = add_color(g)

    return g

def add_color(g):
    '''
    Helper function to add Blue and Red color to the graph.

    @param  Graph   g: graph that needs the colors.

    @return Graph   g: updated graph that has the correct colors for Blue and Red Agents.
    '''
    mappingblue = {blue:'Blue'}
    mappingred = {red:'Red'}
 
    g = nx.relabel_nodes(g, mappingblue)    # changes label of Blue in graph from memory location to 'Blue'
    g = nx.relabel_nodes(g, mappingred)     # changes label of Red in graph from memory location to 'Red'
    return g

def start_game():
    '''
    Initializes the days and starts a new game.
    '''
    global days, changed_votes, energy_used     # will be used to track how many rounds have passed
    
    days = 0
    energy_depleted = False
    changed_votes = 0
    energy_used = []
    avg = blue.energy
    use_grey_agent = False

    while(days != ELECTION_DAY):

        if blue.energy <= 0:        # checks Blue Agents energy each round
            energy_depleted = True
            if VERBOSE:
                print(f"\nBlue agent has depleted its energy! Blue team loses!\n")
                print(f"break!")
            break

        if blue.energy < avg:      # check if current Blue energy is less than avg
            use_grey_agent = True
        else:
            use_grey_agent = False

        curr_energy = blue.energy
        next_round(use_grey_agent)  # commences the next round
        energy_used.append(curr_energy - blue.energy)
        avg = mean(energy_used)     # gets avg of energy used

    winner = end_game(energy_depleted)       # ends the game
    return winner

def next_round(use_grey_agent):
    '''
    Function used to run all the teams turns.
    If user chose to play as Blue Agent, 
    If user chose to play as Red Agent, game will prompt the user to input a number (1-5) for
    message potency of the Red Agent broadcast.

    @param  boolean     use_grey_agent: variable to show whether Grey Agent will be used this round or not.
    '''
    global days
    global changed_votes

    start = time.time()
    if VERBOSE:
        print("\n----------------------------------------------------")
        print(f"\033[1mIt's now day {days}!\033[m")
    days += 1

    if VERBOSE:
        print(f"\n\t\t\033[1;4;32m---GREEN TEAM'S TURN---\033[0m\n")
    for edges in updated_graph.edges:       # Green interaction is run for every Green Agent
        if edges[1] == 'Red' or edges[1] == 'Blue':
            continue
        green[edges[0]].green_interaction(updated_graph, green, edges[0], edges[1])
    
    vote_count = 0
    not_vote_count = 0
    for agents in green:        # votes are counted for Red Agent to use
        if green[agents].vote:
            vote_count += 1
        else:
            not_vote_count += 1

    if VERBOSE:
        print(f"\n\t\t\033[1;4;34m---BLUE TEAM'S TURN---\033[0m\n")
        # commence Blue Agents turn       
        print(f"\033[1;4;34m---BLUE IS DECIDING WHETHER TO USE GREY AGENT!---\033[0m\n")
    # Blue agent randomly chooses if it wants to use a Grey Agent
    if use_grey_agent == True:
        # commence Grey Agents turn
        if VERBOSE:
            print("Blue decided to use grey\n")
        grey_turn()
    else:
        if VERBOSE:
            print("Blue decided not to use grey")
        blue.blue_turn(updated_graph, green, player_team)
    
    if VERBOSE:
        print(f"\n\t\t\033[1;4;31m---RED TEAM'S TURN---\033[0m\n")
    # commence Red Agents turn
    changed_votes += red.red_turn(updated_graph, green, vote_count, not_vote_count, player_team)
    if VERBOSE:
        print(f"Red team successfully affected the uncertainties {changed_votes} times!")

    end = time.time()
    total_time = end - start
    if VERBOSE:
        print(f"Round {days} took {total_time}s to run!")

def grey_turn():
    '''
    Function used to run Grey Agents turns.
    Function will randomly choose a Grey Agent from Grey list and check whether
    it is a Red spy or not. If it is, it'll run a Red Agent function. Else, it'll run a
    Blue Agent function.
    '''
    agent = random.choice(grey_keys)

    if grey[agent].used == False:       # checks if chosen Agent has been used before
        if VERBOSE:
            print(f"Blue chose to use Grey agent {'Grey'+str(grey[agent].id)}!\n")

        if grey[agent].team == 'Blue':  # checks if chosen Agent has allegiance to Blue
            grey[agent].grey_turn_blue(updated_graph, green)

        else:                           # otherwise, chosen Agent is a Red spy
            if VERBOSE:
                print(f"Grey agent {grey[agent].id} turned out to be a Red spy!\n")
            grey[agent].grey_turn_red(updated_graph, green)
    
    else:   
        if VERBOSE:                            # Grey Agent is skipped if it has been used
            print(f"Grey agent {'Grey'+str(grey[agent].id)} has been used, moving on to next round!\n")

def end_game(energy_depleted):
    '''
    Displays which team won, how many green agents decided to vote/not vote and exits the game.
    This function uses ANSI escape code to bold, italicize and change color of some words.
    Use the following link for guide:
    >>[https://ozzmaker.com/add-colour-to-text-in-python/]<<

    @param  boolean     energy_depleted: bool value to denote whether Blues energy has been depleted or not
    '''
    global updated_graph

    winner = ''

    if VERBOSE:
        print(f"Green ID\t Green Uncertainty\t    Voting Status")
        for agent in green:
            print(f"{green[agent].id}\t\t{green[agent].uncertainty}\t\t{green[agent].vote}")

    green_members = len(green)
    green_votes = 0
    green_no_votes = 0
    for agent in green:
        if green[agent].vote == True:       # counts how many Green Agents voted
            if updated_graph.has_edge('Red', agent):
                updated_graph.remove_edge('Red', agent)
                updated_graph.add_edge('Blue', agent)
            green_votes += 1
        else:                               # counts how many Green Agents did not vote
            if updated_graph.has_edge('Blue', agent):
                updated_graph.remove_edge('Blue', agent)
                updated_graph.add_edge('Red', agent)
            green_no_votes += 1

    updated_graph = add_color(updated_graph)
    if VERBOSE:
        nx.draw_shell(          # draws final version of the graph
                updated_graph,      
                node_color=color_map,
                with_labels=True, 
                node_size=1000
                )

    if VERBOSE:
        if energy_depleted:     # check if Blue Agent has used up all its energy
            winner = 'Red'
            print("\n\t\t\t---\033[1;3mSUDDEN LOSS\033[0m---\n")
            print("It looks like \033[1;4;34mBlue\033[0m team has depleted all their energy!")
            print("Therefore, \033[1;4;34mBlue\033[0m team automatically loses and \033[1;4;31mRed\033[0m team wins!")
            print(f"Of the {green_members} green agents, they successfully affected the uncertainties of {changed_votes} green agent(s) in total!\n")
            print(f"The ratio of voters to non-voters is as follows:\n")
            print(f"{tb([[green_votes, green_no_votes]], headers=['VOTING','NOT VOTING'], tablefmt='fancy_grid',stralign='center',numalign='center')}")
            print("Let's have a look at the final network!\n")
            plt.show()  # visualizes the final version of the graph
            plt.clf()   # clears the current graph
            return winner
            
        else:                   # game ended with Blue Agent having remaining energy
            print("\n\t\t\t---\033[1;3mELECTION DAY\033[0m---\n")
            print("It's election day! Let's see how many of the green agents decided to vote!")
            print(f"Of the {green_members} green agents, the ratio of voters to non-voters is:\n")
            print(f"{tb([[green_votes, green_no_votes]], headers=['VOTING','NOT VOTING'], tablefmt='fancy_grid',stralign='center',numalign='center')}")
            print("")
            if green_votes > green_no_votes:        # Blue wins if total number of Green voters is greater than non-voters
                winner = 'Blue'
                print(f"\033[1;4;34mBlue\033[0m team won! They had {blue.energy} energy remaining!\n")
                plt.show()
                plt.clf()
                return winner
            
            elif green_votes == green_members:      # special case where the number of voters equals to the number of Green Agents
                winner = 'Blue'
                print(f"WHAT A CRAZY WIN BY \033[1;4;34mBLUE\033[0m TEAM!!!")
                print(f"THEY SUCCESSFULLY MADE ALL {green_members} VOTE!!! DAMN!!\n")
                plt.show()
                plt.clf()
                return winner

            elif green_votes == green_no_votes:     # neither team wins if number of voters and non-voters are the same (tie)
                winner = 'Tie'
                print(f"Hmm, that's weird! There's an equal number of voters and non-voters!")
                print(f"Looks like it's a tie! Here are the results for this match:\n")
                print(f"\t\033[1;4;34mBlue\033[0m team had {blue.energy} energy remaining!")
                print(f"\t\033[1;4;31mRed\033[0m team successfully affected the uncertainties of {changed_votes} green agents!\n")
                plt.show()
                plt.clf()
                return winner

            else:                                   # Red team wins otherwise
                winner = 'Red'
                print(f"\033[1;4;31mRed\033[0m team won! Of the {green_no_votes} green agents who decided not to vote,\nthey successfully affected the uncertainties of {changed_votes} green agent(s) in total!\n")
                plt.show()
                plt.clf()
                return winner

    else:
        if energy_depleted:
            winner = 'Red'
            print("\033[1;4;31mRed\033[0m Team won")
            plt.clf()
        elif green_votes > green_no_votes:
            winner = 'Blue'
            print("\033[1;4;34mBlue\033[0m Team won")
            plt.clf()
        elif green_no_votes > green_votes:
            winner = 'Red'
            print("\033[1;4;31mRed\033[0m Team won")
            plt.clf()
        elif green_votes == green_no_votes:
            winner = 'Tie'
            print("Tie")
            plt.clf()

        print(f"{tb([[green_votes, green_no_votes]], headers=['VOTING','NOT VOTING'], tablefmt='fancy_grid',stralign='center',numalign='center')}")
        return winner


def main():
    '''
    Main function for auto_gamefile.py.
    This function will ask the user for the number of Green Agents to be initialized in the game.
    This function will also ask the user for an input which will determine whether a user wants to play
    as either a Red Agent or Blue Agent.
    Afterwards, the game will begin.
    '''
    global player_team, ELECTION_DAY, VERBOSE

    start = time.time()

    verbose = input("Please type '-v' if you would like a detailed output of every round!\nIf not, just hit ENTER!\n")
    if verbose == '-v':
        VERBOSE = True
    else:
        VERBOSE = False

    set_verbose(verbose)

    game_loop = input("If you would like the game to loop under a number of times, enter a positive number, if not hit ENTER:\n")
    if game_loop == '':
        game_loop = 1
    
    num_nodes = input("How many green nodes would you like?\n")    # get user input for their desired number of green nodes
    if num_nodes == '':
        num_nodes = 20
    num_nodes = int(num_nodes)

    player_team = input("\nWhich team would you like to play as?\nPlease type either of the teams [\033[1;31mRed\033[0m] or [\033[1;34mBlue\033[0m] :D\nIf you would like the game to run automatically, just hit ENTER!\n")
    print(f"You have chosen [{player_team}]!\n")

    ELECTION_DAY = input("Lastly, how many rounds would you like the game to last for?\nPlease choose a positive number: ")
    if ELECTION_DAY == "":      # ELECTION_DAY defaults to a value between 23 and 31 if no input is given
        ELECTION_DAY = random.randint(23,31)
    ELECTION_DAY = int(ELECTION_DAY)
    print(f"You have chosen for the game to last for {ELECTION_DAY} days!\n")

    print("Game commences\n\n")


    if int(game_loop) > 1:
        red_wins = 0
        blue_wins = 0
        no_wins = 0
        for x in range(int(game_loop)):
            print(f"\nRunning game: {x+1} out of {game_loop}")
            generate_network(num_nodes)
            winner = start_game()
            if winner == 'Red':
                red_wins += 1
            if winner == 'Blue':
                blue_wins += 1
            if winner == 'Tie':
                no_wins += 1
        if int(game_loop) > 1:
            print(f"Red - {red_wins}/{game_loop}")
            print(f"Blue - {blue_wins}/{game_loop}")
            print(f"Neither wins - {no_wins}/{game_loop}")
            print("")
    else:
        
        generate_network(num_nodes)
        winner = start_game()

    end = time.time()
    total_time = end - start
    if VERBOSE:
        print(f"The game took {total_time}s to run in total!\n")
    
    return

if __name__ == "__main__":
    main()