import regex as re ,os
from typing import List, NamedTuple
from praatio import tgio

class Utils:
    def __init__(self, consonants_filename, double_consonants_filename, nazalized_consonants_filename, double_vowels_filename, vowels_filename, glide_filename, syllables_filename) -> None:
        self.consonants = "".join(self.get_file_contents(consonants_filename))
        self.double_consonants = "|".join(self.get_file_contents(double_consonants_filename))
        self.nazalized_consonants = "".join(self.get_file_contents(nazalized_consonants_filename))
        self.double_vowels = "|".join(self.get_file_contents(double_vowels_filename))
        self.vowels = "".join(self.get_file_contents(vowels_filename))
        self.glide = "".join(self.get_file_contents(glide_filename))
        self.syllables = self.get_file_contents(syllables_filename)
        self.syllables.sort(key=len, reverse=True)
        self.syllables.insert(0, self.syllables.pop())


    @staticmethod
    def encode(word: str) -> str:
        encodings = ["k͡ |kp","n̄|ng","ɲ|ny","ō|oo","ā|aa","ē|ee","ī|ii","ō|oo","ū|uu","ū|uu","Ō|OO","Ā|AA","Ē|EE","Ī|II","Ū|UU",]
    
        for line in encodings:
            replacement, character = line.split("|")
            word = word.replace(character.strip(), replacement.strip())
        return word

    
    @staticmethod
    def decode(word: str) -> str:
        encodings = ["k͡ |kp","n̄|ng","ɲ|ny","ō|oo","ā|aa","ē|ee","ī|ii","ō|oo","ū|uu","ū|uu","Ō|OO","Ā|AA","Ē|EE","Ī|II","Ū|UU",]
        
        for line in encodings:
            replacement, character = line.split("|")
            word = word.replace(replacement.strip(), character.strip())
        return word

    
    def get_file_contents(self, filename: str) -> List[str]:

        with open(filename) as f:
            
            l = [Utils.encode(x).strip().replace(" ", "-") for x in f.readlines()]
            
            
            return l


    def build_pattern(self, syllable: str)-> str:
        result = ""
        
        for char in syllable:
            if len(syllable) == 1 and char == "V":
                return rf"^({self.double_vowels}|[{self.vowels}])"
            elif len(syllable) == 1 and char == "N":
                return rf"^[{self.nazalized_consonants}]"
            elif char == "C":
                result = rf"{result}([{self.consonants}]|{self.double_consonants})"
            elif char == "V":
                result = rf"{result}({self.double_vowels}|[{self.vowels}])"
            elif char == "G":
                result = rf"{result}([{self.glide}])"
        return rf"^{result}"

    def syllabify(self, word: str) -> List[str]:

        word = word.strip()
        word = word.strip("-")

        match: str = ''
        next_match: str = ''
            
        for syllable in self.syllables:
            
            # build regex pattern for the syllable

            # if in_context and len(syllable) == 1:
            #     continue
            pattern = self.build_pattern(syllable)
        
            # return first match
            
            m = re.search(pattern, word)
            match = m.group() if m else "" 
            
            
            # get sequences after the match
            nm = re.search(rf"(?<={pattern}).*", word) 
            next_match = nm.group() if nm else "" 


            
            if match and next_match:           # if we have a match and if there are characters after the match
                # print("match:", m, "next_match:", nm, "pattern:", pattern) 
            
                if len(match) == 1 and (match[-1]+next_match[0]) in self.double_consonants:
                    continue

                if next_match[0] in self.consonants or next_match[0] == "-":     # if character after match is a consonant break out of loop
                    break
            elif match and not next_match: # if we have a match and if there are no characters after the match we break
                break
        
        return [match, next_match]
    
    def process_textgrid(self,textgrid_filename: str, syllables_list_filename: str) -> None:

        tg = tgio.openTextgrid(textgrid_filename, readRaw=True)
        syllables = tg.tierDict['syllables']
        report = open("results/report.csv", "w+")
        report.write("word,discovered syllables,number of syllables,number of boundaries,error\n")


        with open(syllables_list_filename) as f:
            interval_list: list = list()
            entry_list: list = list()
            for entry in syllables.entryList:
                if entry.label == "pause":

                    discovered_syllable = next(f)
                    syllable = discovered_syllable.strip().split("-")
                    word = "".join(syllable)
                    entry_list_size = len(entry_list)
                    syllable_size = len(syllable)


                    if entry_list_size == syllable_size:
                        for item, syl in zip(entry_list, syllable):
                            interval_list.append(Entry(item.start, item.end, syl))
                        
                        interval_list.append(Entry(entry.start, entry.end, entry.label))

                        report.write(f"{word},{discovered_syllable.strip()},{syllable_size},{entry_list_size},no error\n")
                    

                    elif entry_list_size < syllable_size:
                        index = entry_list_size - 1

                        
                    
                        for item, syl in zip(entry_list, syllable[:index]):
                            interval_list.append(Entry(item.start, item.end, syl))

                        last_item = entry_list[-1]
                        remaining_syllables = "-".join(syllable[index:])
                        interval_list.append(Entry(last_item.start, last_item.end, remaining_syllables))
                        interval_list.append(Entry(entry.start, entry.end, entry.label))

                        report.write(f"{word},{discovered_syllable.strip()},{syllable_size},{entry_list_size},syllables not equal\n")



                    else:
                        for index in range(len(entry_list)):
                            try:
                                interval_list.append(Entry(entry_list[index].start, entry_list[index].end, syllable[index]))
                            except IndexError:
                                interval_list.append(Entry(entry_list[index].start, entry_list[index].end, entry_list[index].label))

                        
                        interval_list.append(Entry(entry.start, entry.end, entry.label))

                        report.write(f"{word},{discovered_syllable.strip()},{syllable_size},{entry_list_size},syllables not equal\n")


                    entry_list = []

                else:
                    entry_list.append(entry)

        report.close()

        new_tier = tgio.IntervalTier("syllables", interval_list)

        tg.replaceTier("syllables", new_tier)

        textgrid_results_file_name, textgrid_results_file_extention = os.path.splitext(textgrid_filename.split("/")[-1])
        tg.save(f"results/{textgrid_results_file_name}_results{textgrid_results_file_extention}", useShortForm=False)



class Entry(NamedTuple):
    start: float
    end: float
    label: str

if __name__ == "__main__":

    pass