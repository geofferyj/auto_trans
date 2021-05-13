from auto_trans.utils import Utils
from typing import List
from auto_trans.tree import Tree
import os


class Main:
    def __init__(self, 
    words_filename,
    consonants_filename, 
    double_consonants_filename, 
    nazalized_consonants_filename, 
    double_vowels_filename, 
    vowels_filename, 
    glide_filename, 
    syllables_filename, text_grid_filename) -> None:

        self.text_grid_filename = text_grid_filename
        self.consonants_filename = consonants_filename
        self.double_consonants_filename = double_consonants_filename
        self.nazalized_consonants_filename = nazalized_consonants_filename
        self.double_vowels_filename = double_vowels_filename
        self.vowels_filename = vowels_filename
        self.glide_filename = glide_filename
        self.syllables_filename = syllables_filename     
        self.words_filename = words_filename   
     


    def run(self):
        utils = Utils(
            self.consonants_filename,
            self.double_consonants_filename,
            self.nazalized_consonants_filename,
            self.double_vowels_filename,
            self.vowels_filename,
            self.glide_filename,
            self.syllables_filename)


        words: List[str] = utils.get_file_contents(self.words_filename)
        syllabification_result_filename = "results/syllabification_result.txt"
        os.makedirs("results", exist_ok=True)
        with open(syllabification_result_filename,"w+") as file:

            for word in words:
                tree = Tree(utils)
                tree.create(word)
                leaves = tree.get_leaves()
                syllable = "-".join(leaves)

                file.writelines(f"{utils.decode(syllable)}\n")

        utils.process_textgrid(self.text_grid_filename, syllabification_result_filename)
