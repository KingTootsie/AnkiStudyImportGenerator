if __name__ == "__main__":
    #IMPORTS
    import genanki
    import os, sys
    import random

    #FUNCTIONS
    def search_for_decks() -> list[str]:
        confirmed_deck_paths = []

        files = os.scandir("./decks/")
        for file in files:
            if file.name.endswith(".txt"):
                with open(file.path, "r") as deck:
                    line_one = deck.readlines(0)[0].replace("\n", "")

                    if line_one == "[DECK]":
                        confirmed_deck_paths.append(file.path)
                
        return confirmed_deck_paths
    
    def user_deck_select() -> str:
        deck_paths = search_for_decks()
        
        print("Here are the following decks I found:")

        for num, path in enumerate(deck_paths):
            file_name = os.path.basename(path)
            print(f"{num + 1} - {file_name}")

        print("")
        while True:
            chosen_deck = input("Enter the number for the deck you want converted: ")
            if chosen_deck == "":
                print("This cannot be blank.")
            else:
                if chosen_deck.isdigit():
                    chosen_deck = int(chosen_deck)
                    if chosen_deck <= 0 or chosen_deck > len(deck_paths):
                        print("You must pick a number given for a deck.")
                    else:
                        break
                else:
                    print("You must put an integer.")

        return deck_paths[chosen_deck - 1]
    
    def format_deck(deck_path: str) -> list:
        with open(deck_path, "r") as file:

            cards = []
            lines = file.readlines()
            
            for line in lines[1:]:
                line.replace("\n", "")

                cut_off = line.find("--")

                term = line[:cut_off]
                definition = line[cut_off + 2:]

                #print(f"{term} - {definition}")
                cards.append([term, definition])

        return cards
    
    def create_anki_package(cards: list):
        deck_id = random.randrange(1 << 30, 1 << 31)

        while True:
            deck_name = input("Enter a deck name: ")
            if deck_name == "":
                print("This cannot be blank.")
            else:
                break
        
        deck = genanki.Deck(deck_id, deck_name)

        model = genanki.Model(
            random.randrange(1 << 30, 1 << 31),
            'Model',
            fields=[
                {'name': 'Term'},
                {'name': 'Definition'},
            ],
            templates=[
                {
                    'name': 'Card 1',
                    'qfmt': '{{Term}}',
                    'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}',
                },
            ])

        for card in cards:
            note = genanki.Note(model=model, fields=card)
            deck.add_note(note)

        genanki.Package(deck).write_to_file('output.apkg')

    #MAIN
    deck_path = user_deck_select()

    cards = format_deck(deck_path=deck_path)

    create_anki_package(cards=cards)
    
