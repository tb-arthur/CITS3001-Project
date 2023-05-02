'''
    ------- MADE BY: -------
        Sean Lim            22321345
Athhar Daffa Djajasantosa   22676919

agents.py is a file used to store class declarations and functions
of the following teams:
    -> Green
    -> Blue
    -> Red
    -> Grey
'''
from math import pi
from tabulate import tabulate as tb
from auto_gamefile import *
import random

def set_verbose(verbose):
    global VERBOSE
    if verbose == '-v':
        VERBOSE = True
    else:
        VERBOSE = False

class Green:
    '''
    Class for Green Team
    '''
    def __init__(self, id:int):
        '''
        Constructor for Green Agents
        
        @param  int      id: id for the Green Agent

        @self   boolean  vote:   boolean value that denotes whether Agent will vote or not
        @self   float    uncertainty: probability whether Agent opinion will change
        '''
        self.id = id
        #new way
        opinion = random.choices([True, False], weights=(65,35))[0]
        self.vote = opinion
        self.uncertainty = round(random.uniform(-1, 1), 1)

    def green_interaction(self, g, green_team, node_1, node_2):
        '''
        Function used to simulate interactions between Green Agents.

        @param Graph    g: graph of the network.
        @param dict     green_team: dictionary that contains Green Agents.
        @param Green    node_1: original node that we access.
        @param Green    node_2: neighbor of the original node.
        '''
        
        if g.has_edge(node_1, node_2):
            #print(f"{node_1} --> {node_2}")
            #print(f"There's an edge between {green_team[node_1].id} and {green_team[node_2].id}!")
            node1_uncertainty = green_team[node_1].uncertainty
            node2_uncertainty = green_team[node_2].uncertainty

            opinion_change = [True, False]
            # In real world, not many people will change political alignment easily
            PERCENTAGE_YES = 80
            PERCENTAGE_NO = 20

            if node1_uncertainty < node2_uncertainty: # If node1 is less uncertain than node2
                green_team[node_2].uncertainty = node2_uncertainty + 0.25 * (node1_uncertainty - node2_uncertainty)
                #print(f"\t{node2_uncertainty} --> {green_team[node_2].uncertainty}\n")
                
                if green_team[node_2].uncertainty > 0:   # node2 rethinking their opinion
                    new_opinion = random.choices(opinion_change, weights=(PERCENTAGE_YES,PERCENTAGE_NO))[0]
                    #print(f"{green_team[node_2].vote} --> {new_opinion}")
                    if new_opinion:
                        green_team[node_2].vote = green_team[node_1].vote
                else:   # node2 is certain with their opinion
                    PERCENTAGE_YES = 5
                    PERCENTAGE_NO = 95
                    new_opinion = random.choices(opinion_change, weights=(PERCENTAGE_YES,PERCENTAGE_NO))[0]
                    #print(f"{green_team[node_2].vote} --> {new_opinion}")
                    if new_opinion:
                        green_team[node_2].vote = green_team[node_1].vote

            elif node1_uncertainty > node2_uncertainty: # If node1 is more uncertain than node2
                green_team[node_1].uncertainty = node1_uncertainty + 0.25 * (node2_uncertainty - node1_uncertainty)
                #print(f"\t{node1_uncertainty} --> {green_team[node_1].uncertainty}")
                
                if green_team[node_1].uncertainty > 0:   # node1 rethinking their opinion
                    new_opinion = random.choices(opinion_change, weights=(PERCENTAGE_YES,PERCENTAGE_NO))[0]
                    #print(f"{green_team[node_1].vote} --> {new_opinion}")
                    if new_opinion:
                        green_team[node_1].vote = green_team[node_2].vote
                else:   # node1 is certain with their opinion
                    PERCENTAGE_YES = 5
                    PERCENTAGE_NO = 95
                    new_opinion = random.choices(opinion_change, weights=(PERCENTAGE_YES,PERCENTAGE_NO))[0]
                    #print(f"{green_team[node_1].vote} --> {new_opinion}")
                    if new_opinion:
                        green_team[node_1].vote = green_team[node_2].vote


class Blue:
    '''
    Class for Blue Team
    '''
    def __init__(self, id:int, energy:int):
        '''
        Constructor for Blue Agent.
        
        @param int  id: id for the Blue Agent.
        @param int  energy: acts as the Blue Agents "life-line".
        '''
        self.id = id
        self.energy = energy

    def blue_turn(self, g, green_team, player):
        '''
        Function for Blue Agent to change the opinions of Green Agents.

        @param Graph   g: graph that contains network of Green Agents.
        @param dict    green_team: dictionary of Green Agents.
        @param str     player: variable that shows which team the player chose.
        '''
        if VERBOSE:
            print(f"It's now Blue agent's turn! Blue agent has {self.energy} energy left.")
        #print(f"Blue agent used \033[1;3m""COUNTER-NARRATIVE""\033[0m!")

        message_list = [
                    "\033[1mBlue Team proclaims that they will provide more support for LGBTQIA+ community\033[0m",
                    "\033[1mBlue Team reduce public transport fees by 30%\033[0m",
                    "\033[1mBlue Team announces that climate change will be its priority\033[0m",
                    "\033[1mBlue Team promises to donate $2 million to charity\033[0m",
                    "\033[1mBlue Team guarantees that they will increase job opportunities for everyone including fresh graduates\033[0m",
                    "\033[1mBlue Team assures everyone that they will subsidise health care policies for under-privileged communities\033[0m",
                    "\033[1mBlue Team declares that everyone will be treated equally and without discrimination\033[0m",
                    "\033[1mBlue Team will enforce the rule to allow non-essential workers to work from home\033[0m",
                    "\033[1mBlue Team pledges to use $30 million dollars to alleviate students' debt\033[0m",
                    "\033[1mBlue Team swears to reduce violent crimes in the country by 80% within the next 5 years\033[0m"
                ]
        message_potency = [ 1.2, 1.5, 1.9, 2.3, 2.8, 3.4, 4.1, 4.9, 5.8, 6.8 ]
        chosen_message = random.randint(0, 9)
        # If player is playing as Blue agent
        if player == 'Blue':
                print(f"It's up to you to choose Blue's \033[1;3m""COUNTER-NARRATIVE""\033[0m!")
                print("Choose the level of message potency from 0 to 9\n")
                chosen_message = int(input("You have chosen: "))
        if VERBOSE:
            print(tb([[message_list[chosen_message]]],tablefmt='fancy_grid',stralign='center'),"\n")

        for agent in green_team:
            if self.energy <= 0:
                break
            if g.has_edge('Blue', agent) == True:   # if there's an edge between Blue and Green Agent
                curr_uncertainty = green_team[agent].uncertainty
                curr_vote = green_team[agent].vote
                
                # If the Green Agent is certain about their vote and are not voting, they might change their vote
                if curr_uncertainty < 0 and curr_uncertainty >= -1 and curr_vote == False:
                    PERCENTAGE_NO = 90
                    PERCENTAGE_YES = 10
                    opinion_change = [True, False]
                    new_opinion = random.choices(opinion_change, weights=(PERCENTAGE_YES,PERCENTAGE_NO))[0]
                    # If opinion changed, change the vote
                    if new_opinion:
                        temp = green_team[agent].vote
                        green_team[agent].vote = True
                        if VERBOSE:
                            print(f"{green_team[agent].id} used to be {temp}, now they are {green_team[agent].vote}!")
                            print(f"Blue Agent successfully changed the opinion of {green_team[agent].id}!")
                    
                    
                    self.energy -= abs(curr_uncertainty) * 5 * message_potency[chosen_message]   # depletes LARGE amount of energy by uncertainty
                
                # If the Green Agent is uncertain about their vote and are not voting, they will change their vote
                if curr_uncertainty < 0 and curr_uncertainty <= 1 and curr_vote == False:
                    temp = green_team[agent].vote
                    green_team[agent].vote = True
                    self.energy -= abs(curr_uncertainty) * 2.5  * message_potency[chosen_message]    # depletes MEDIUM amount of energy by uncertainty
                    if VERBOSE:
                        print(f"{green_team[agent].id} used to be {temp}, now they are {green_team[agent].vote}!")
                        print(f"Blue Agent successfully changed the opinion of {green_team[agent].id}!")
                
                # If the Green Agent is already choosing to vote, decrease uncertainty    
                elif curr_vote == True:
                    green_team[agent].uncertainty = curr_uncertainty - abs(0.25 * (0.5 - curr_uncertainty))
                    self.energy -= abs(curr_uncertainty) * 2     # depletes energy by uncertainty
                    if VERBOSE:    
                        print(f"Changed uncertainty: {curr_uncertainty} --> {green_team[agent].uncertainty}")

        if VERBOSE:
            print(f"\nRemaining energy: {self.energy}")


class Red:
    '''
    Class for Red Team
    '''
    def __init__(self, id:int):
        '''
        Constructor for Red Agent.
        
        @param int  id: id for the Red Agent.
        '''
        self.id = id

    def red_turn(self, g, green_team, vote_count, not_vote_count, player):
        '''
        Red teams function which sends out a broadcasting message across all Green Agents.
        The broadcasting message aims to increase a Green Agents uncertainty and make them hesitant with their opinions.

        @param Graph    g: graph that contains network of Green Agents.
        @param dict     green_team: dictionary of Green Agents.
        @param int      vote_count: number of Green Agents that are currently voting.
        @param int      not_vote_count: number of Agents that are currently not voting.
        @param str      player: variable that shows which team the player chose.

        @return int     change_uncertainty_count: number of Green Agents whose uncertainty has been affected because of Red.
        '''
        if VERBOSE:
            print(f"It's now Red agent's turn!")
        #if percentage of ppl (their opinion) == high, then they broadcast
        change_uncertainty_count = 0
        total_count = vote_count + not_vote_count
        if vote_count > not_vote_count:
            send_broadcast = True
        else:
            broadcast_true_false = [True, False]
            send_broadcast_percent = [(vote_count/total_count)*100, (not_vote_count/total_count)*100]
            send_broadcast = random.choices(broadcast_true_false, weights=(send_broadcast_percent[0],send_broadcast_percent[1]))[0]
        if send_broadcast:
            if VERBOSE:
                print(f"Red agent used \033[1;3m""POLITICAL AGENDA""\033[0m!\n")
            message_potency = random.randint(1,5)
            if player == 'Red':
                print(f"It's up to you to choose the message potency!")
                print("Choose from the following: 1, 2, 3, 4, 5\n")
                message_potency = int(input("You have chosen: "))
                #print(f"You have chosen: {message_potency}\n")
            if VERBOSE:    
                print(f"Red has chosen to broadcast a message at potency level: {message_potency}")
            if VERBOSE:
                match message_potency:
                    case 1:
                        print(tb([["\033[1mA rumor is slowly arising about how the Blue Agent has taken part in scandalous acts!\033[0m"]],tablefmt='fancy_grid',stralign='center'))
                    case 2:
                        print(tb([["\033[1mReports suggest that the Blue Agent has been found guilty of corruption!\033[0m"]],tablefmt='fancy_grid',stralign='center'))
                    case 3:
                        print(tb([["\033[1mReports have come out about how the Blue Agent is actually rigging the elections!\033[0m"]],tablefmt='fancy_grid',stralign='center'))
                    case 4:
                        print(tb([["\033[1mBREAKING NEWS!!!! BLUE AGENT HAS BEEN ACCUSED OF BEING RACIST!!\033[0m"]],tablefmt='fancy_grid',stralign='center'))
                    case 5:
                        print(tb([["\033[1mBREAKING NEWS!!!! Rumors have spread about how Blue Agent will abuse the country's\nresources to build more nuclear bombs and take over the entire world!!!\033[0m"]],tablefmt='fancy_grid',stralign='center'))
                print("")
            green_no_vote = {}
        
            for agent in green_team:
                if green_team[agent].vote == False:
                    green_no_vote[agent] = green_team[agent].uncertainty
            green_no_vote = dict(sorted(green_no_vote.items(), key=lambda item: item[1]))
            if message_potency == 4:
                #print(green_no_vote)
                PERCENTAGE_UNFOLLOWED = 0.20
                total_unfollowed = round(len(green_no_vote)*PERCENTAGE_UNFOLLOWED)
                unfollow_dict = dict(list(green_no_vote.items())[:total_unfollowed])
                #print(unfollow_dict)
            if message_potency == 5:
                #print(green_no_vote)
                PERCENTAGE_UNFOLLOWED = 0.25
                total_unfollowed = round(len(green_no_vote)*PERCENTAGE_UNFOLLOWED)
                unfollow_dict = dict(list(green_no_vote.items())[:total_unfollowed])
                #print(unfollow_dict)

            for agent in green_team:
                curr_uncertainty = green_team[agent].uncertainty
                if g.has_edge('Red', agent): # If Agent is following Red news
                    if green_team[agent].vote == True: # If Green Agent votes for Blue
                        match message_potency:
                            case 1:
                                green_team[agent].uncertainty = curr_uncertainty + (0.25 * (0.25 - curr_uncertainty))
                                change_uncertainty_count += 1
                                if VERBOSE:
                                    print(f"Red affected Green uncertainty from: {curr_uncertainty} --> {green_team[agent].uncertainty}")
                                
                            case 2:
                                green_team[agent].uncertainty = curr_uncertainty + (0.35 * (0.25 - curr_uncertainty))
                                change_uncertainty_count += 1
                                if VERBOSE:
                                    print(f"Red affected Green uncertainty from: {curr_uncertainty} --> {green_team[agent].uncertainty}")

                            case 3:
                                green_team[agent].uncertainty = curr_uncertainty + (0.45 * (0.25 - curr_uncertainty))
                                change_uncertainty_count += 1
                                if VERBOSE:
                                    print(f"Red affected Green uncertainty from: {curr_uncertainty} --> {green_team[agent].uncertainty}")

                            case 4:
                                green_team[agent].uncertainty = curr_uncertainty + (0.55 * (0.25 - curr_uncertainty))
                                change_uncertainty_count += 1
                                if VERBOSE:
                                    print(f"Red affected Green uncertainty from: {curr_uncertainty} --> {green_team[agent].uncertainty}")

                            case 5:
                                green_team[agent].uncertainty = curr_uncertainty + (0.65 * (0.25 - curr_uncertainty))
                                change_uncertainty_count += 1
                                if VERBOSE:
                                    print(f"Red affected Green uncertainty from: {curr_uncertainty} --> {green_team[agent].uncertainty}")
                    
                    else: # If Agent already chose not to vote, they are more confident
                        green_team[agent].uncertainty *= -0.02
                        if message_potency >= 4:
                            if (green_team[agent].id in unfollow_dict):
                                if VERBOSE:
                                    print(f"{green_team[agent].id} has had enough of the Red Agent and decided to unfollow them on social media!\n")
                                green_team[agent].vote = True
                                g.remove_edge('Red', agent)

        else:
            if VERBOSE:
                print("Red agent chose to do nothing! Everyone's happy!\n")
        
        return change_uncertainty_count


class Grey:
    '''
    Class for Grey Team
    '''
    def __init__(self, id:int):
        '''
        Constructor for Grey Agents
        
        @param int  id: id for the Grey Agent.
        '''
        self.id = id
        self.used = False
        allegiance = ['Blue', 'Red']
        allegiance_choice = random.choices(allegiance, weights=(69,31))[0]
        self.team = allegiance_choice
    
    def grey_turn_blue(self, g, green_team):
        '''
        This function acts similarly to Blue team's blue_turn() function.
        Grey Agent will act as a Blue Agent and gets another chance of interaction without losing their energy.

        @param Graph    g: graph of network used to check for connections
        @param dict     green_team: dictionary of Green Agents
        '''
        if VERBOSE:
            print("Grey agent has unveiled their disguise and is now a Blue agent!\n")

        message_list = [
                    "\033[1mBlue Team proclaims that they will provide more support for LGBTQIA+ community\033[0m",
                    "\033[1mBlue Team reduce public transport fees by 30%\033[0m",
                    "\033[1mBlue Team announces that climate change will be its priority\033[0m",
                    "\033[1mBlue Team promises to donate $2 million to charity\033[0m",
                    "\033[1mBlue Team guarantees that they will increase job opportunities for everyone including fresh graduates\033[0m",
                    "\033[1mBlue Team assures everyone that they will subsidise health care policies for under-privileged communities\033[0m",
                    "\033[1mBlue Team declares that everyone will be treated equally and without discrimination\033[0m",
                    "\033[1mBlue Team will enforce the rule to allow non-essential workers to work from home\033[0m",
                    "\033[1mBlue Team pledges to use $30 million dollars to alleviate students' debt\033[0m",
                    "\033[1mBlue Team swears to reduce violent crimes in the country by 80% within the next 5 years\033[0m"
                ]
        chosen_message = random.randint(0, 9)
        if VERBOSE:
            print(tb([[message_list[chosen_message]]],tablefmt='fancy_grid',stralign='center'),"\n")

        for agent in green_team:
            if g.has_edge('Blue', agent) == True:   # if there's an edge between Blue and Green Agent
                curr_uncertainty = green_team[agent].uncertainty
                curr_vote = green_team[agent].vote
                
                # If the Green Agent is uncertain about their vote and are not voting, they will change their vote
                if curr_uncertainty > 0 and curr_uncertainty <= 1 and curr_vote == False:
                    PERCENTAGE_NO = 90
                    PERCENTAGE_YES = 10
                    opinion_change = [True, False]
                    new_opinion = random.choices(opinion_change, weights=(PERCENTAGE_YES,PERCENTAGE_NO))[0]
                    # If opinion changed, change the vote
                    if new_opinion:
                        temp = green_team[agent].vote
                        green_team[agent].vote = True
                        if VERBOSE:
                            print(f"{green_team[agent].id} used to be {temp}, now they are {green_team[agent].vote}!")
                            print(f"Blue Agent successfully changed the opinion of {green_team[agent].id}!")
                    
                # If the Green Agent is certain about their vote and are not voting, they might change their vote
                if curr_uncertainty < 0 and curr_uncertainty <= 1 and curr_vote == False:
                    temp = green_team[agent].vote
                    green_team[agent].vote = True
                    if VERBOSE:
                        print(f"{green_team[agent].id} used to be {temp}, now they are {green_team[agent].vote}!")
                        print(f"Blue Agent successfully changed the opinion of {green_team[agent].id}!")
                
                # If the Green Agent is already choosing to vote, decrease uncertainty    
                elif curr_vote == True:
                    green_team[agent].uncertainty = curr_uncertainty - abs(0.25 * (0.5 - curr_uncertainty))
                    if VERBOSE:    
                        print(f"Changed uncertainty: {curr_uncertainty} --> {green_team[agent].uncertainty}")

        self.used = True

    def grey_turn_red(self, g, green_team):
        '''
        This function acts similarly to Red team's red_turn() function.
        Grey spy can push a highly potent message, without making Red team lose followers.

        @param dict     green_team: dictionary of Green Agents
        '''
        if VERBOSE:
            print(f"Grey agent turned out to be a Red spy!")

        change_uncertainty_count = 0
        
        if VERBOSE:
            print(f"Grey agent used \033[1;3m""POLITICAL AGENDA""\033[0m!\n")

        for agent in green_team:
            curr_uncertainty = green_team[agent].uncertainty
            if g.has_edge('Red', agent):
                if green_team[agent].vote == True: # If green agent votes for blue
                    green_team[agent].uncertainty = curr_uncertainty + (0.65 * (0.25 - curr_uncertainty))#curr_uncertainty - (0.75 * (curr_uncertainty * 0.75)), 3)
                    change_uncertainty_count += 1
                    if VERBOSE:
                        print(f"Red spy affected Green uncertainty from: {curr_uncertainty} --> {green_team[agent].uncertainty}")

        self.used = True